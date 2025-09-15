#!/usr/bin/python3

from flask import Flask, request, jsonify, Response, g
from flask_cors import CORS
from flask import render_template
from flask_wtf.csrf import CSRFProtect, CSRFError

import jwt
import datetime
import time
import json
import os
import bcrypt
import psycopg2
from psycopg2 import sql
import psycopg2.extras

import common.db as db
import common.glb_consts as glb
import common.inmemory as im
import common.utils as u
from system.auth import auth_bp
from send_notifications import notify_bp
from gpio import gpio_bp
from charts import charts_bp
from decorators import auth_required
import system.exec_system_commands as exs

app = Flask(__name__)
CORS(app)

# TODO: активировать защиту CSRF
# app.config['SECRET_KEY'] = glb.SECRET_KEY
# template_dir = os.path.abspath('./templates')
# app.template_folder = template_dir
# csrf = CSRFProtect(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gpio_bp, url_prefix='/gpio')
app.register_blueprint(notify_bp, url_prefix='/notify')
app.register_blueprint(charts_bp, url_prefix='/charts')



# Handle CSRF errors gracefully
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response



# журнал полученных параметров с контроллера СП (по таймауту запрашиваем и сохраняем)
@app.route('/params_log', methods=['GET'])
@auth_required
def params_log():
    # TODO: сделать роли константами
    if g.token_data.get('role') not in ['operator', 'admin']:
        return ''

    limit = request.args.get("limit", type=int)
    start_d, end_d = u.convert_dates(request.args.get("start_date"), request.args.get("end_date"))

    result = db.get_params_log(start_d, end_d, limit)
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })



# журнал того что во внутренней памяти самого контроллера СП лежит (посуточно)
@app.route('/controller_internal_log', methods=['GET'])
@auth_required
def controller_internal_log():
    limit = request.args.get("limit", type=int)
    start_d, end_d = u.convert_dates(request.args.get("start_date"), request.args.get("end_date"))

    print(start_d, end_d, limit)
    result = db.get_controller_internal_log(start_d, end_d, limit)
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })



# журнал событий АК
@app.route('/events_log', methods=['GET'])
@auth_required
def events_log():
    limit = request.args.get("limit", type=int)
    severity = request.args.get("severity")
    event_type = request.args.get("event_type")
    start_d, end_d = u.convert_dates(request.args.get("start_date"), request.args.get("end_date"))

    result = db.get_events_log(start_d, end_d, limit, severity, event_type)
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })



# когда нажимаем кнопку сохранения источника точного времени
@app.route("/apply_time_source", methods=["GET"])
@auth_required
def change_time_source():
    src, addr = db.get_time_source()
    
    db.event_log_add(f'Смена источника времени = {src}, {addr}', 'time', 'EVENT', 'INFO')

    if not src or src not in ['NTP', 'RTC']:
        return jsonify({"error": "Invalid time source"}), 400

    try:
        if src == 'NTP':
            if not addr or not u.is_valid_ntp_server(addr):
                return jsonify({"error": "Invalid NTP server address"}), 400
            exs.update_chrony_config(addr)
        else:
            exs.stop_daemon('chronyd')
    except Exception as e:
        db.event_log_add(f"Error applying time source: {str(e)}", 'time', 'ERROR', 'ERROR')
        return jsonify({"error": "Internal server error"}), 500

    return 'OK'



@app.route("/get_complex_settings", methods=["GET"])
@auth_required
def list_settings():
    return db.get_complex_settings()



@app.route('/clear_events_log')
@auth_required
def clear_events_log():
    db.clear_log('event_log')
    return jsonify(message='OK')



@app.route('/clear_params_log')
@auth_required
def clear_params_log():
    db.clear_log('dynamic_information')
    return jsonify(message='OK')



@app.route("/update_complex_settings/<int:setting_id>", methods=["PUT"])
@auth_required
def update_setting(setting_id):
    if not setting_id or int(setting_id) > 255:
        return jsonify({"error": "Invalid setting_id"}), 400

    data = request.get_json() or {}
    if "value" not in data:
        return abort(400, "Missing value")
    new_value = data["value"]
    return db.update_complex_setting(setting_id, new_value)



@app.route('/set_controller_load_mode', methods=['GET'])
@auth_required
def load_control():
    mode = request.args.get('mode')
    device_id = request.args.get('device_id')

    if not mode or mode not in ['1', '0']:
        return jsonify({"error": "Invalid mode"}), 400
    if not device_id or int(device_id) > 4:
        return jsonify({"error": "Invalid device_id"}), 400

    db.event_log_add(f'{mode}', 'UI: lamp on off', 'EVENT', 'DEBUG')

    cmd = u.create_controller_command(glb.CONTROLLER_CMD_LOAD_MODE)
    cmd['value'] = mode
    im.redis_set('command' + str(device_id), json.dumps(cmd))

    return 'OK'



@app.route('/wifi_set_state', methods=['GET'])
@auth_required
def wifi_set():
    state = request.args.get('state')
    db.event_log_add(f'{state}', 'wifi', 'EVENT', 'INFO')

    if not state or state not in ['on', 'off']:
        return jsonify({"error": "Invalid state"}), 400
    if state == 'on':
        im.redis_set(im.RK_WIFI_ON_REQ, 1)
    if state == 'off':
        im.redis_set(im.RK_WIFI_OFF_REQ, 1)

    return 'OK'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)

