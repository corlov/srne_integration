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


app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gpio_bp, url_prefix='/gpio')
app.register_blueprint(notify_bp, url_prefix='/notify')
app.register_blueprint(charts_bp, url_prefix='/charts')


# TODO: активировать защиту CSRF
# app.config['SECRET_KEY'] = glb.SECRET_KEY
# template_dir = os.path.abspath('./templates')
# app.template_folder = template_dir

# # --- НАСТРОЙКА CSRF ДЛЯ SPA ---
# # Указываем, что токен должен искаться в заголовке X-CSRFToken
# app.config['WTF_CSRF_HEADER_NAME'] = 'X-CSRFToken'
# # Указываем, что токен будет передаваться через cookie
# app.config['WTF_CSRF_TIME_LIMIT'] = 600 # Время жизни токена (1 час)
# app.config['WTF_CSRF_SSL_STRICT'] = False # Для разработки, если у тебя нет HTTPS
# csrf = CSRFProtect(app)

# csrf.exempt(gpio_bp)
# csrf.exempt(charts_bp)

APP_VERSION = os.getenv('APP_VERSION', 'unknown')

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
            im.publish('chrony_updates', addr)
        else:
            im.publish('chrony_updates', '')
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



@app.route('/healthz', methods=['GET'])
def health_check():
    try:
        import redis
        r = redis.StrictRedis(host=im.REDIS_ADDR, port=im.REDIS_PORT, db=0)
        r.set('api_ping', time.time())
        val = r.get('api_ping')
        if not val:
            return jsonify({"status": "error", "details": "redis read error"}), 503

        pin = db.get_pin_by_code('PIN_OUT_K3_LAMP')
        if not pin:
            jsonify({"status": "error", "details": "db read error"}), 503
    except Exception as e:
        return jsonify({"status": "error", "details": f"{str(e)}"}), 503

    return jsonify({"healthZ-status": "OK"}), 200




def init():
    im.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    im.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    glb.SECRET_KEY = os.getenv('SECRET_KEY', 'uw3cok92adxmzpf35_secret_key_value_12082025')
    glb.EXP_LIMIT = int(os.getenv('EXP_LIMIT', 600))

    glb.DB_HOST = os.getenv('DB_HOST', 'localhost')
    glb.DB_NAME = os.getenv('DB_NAME', 'solar_controller_telemetry')
    glb.DB_USER = os.getenv('DB_USER', 'postgres')
    glb.DB_PASSWORD = os.getenv('DB_PASSWORD', 'gen_postgress_password')
    glb.DB_PORT = int(os.getenv('DB_PORT', 5432))

    glb.SSE_UPDATE_GPIO_TIMEOUT = int(os.getenv('SSE_UPDATE_GPIO_TIMEOUT', 5))
    glb.SSE_UPDATE_DYNAMIC_DATA_TIMEOUT = int(os.getenv('SSE_UPDATE_DYNAMIC_DATA_TIMEOUT', 10))
    glb.SSE_UPDATE_COMPLEX_STATUS_TIMEOUT = int(os.getenv('SSE_UPDATE_COMPLEX_STATUS_TIMEOUT', 3))

    glb.PIN_OUT_K2_TRAFFICLIGHT = db.get_pin_by_code('PIN_OUT_K2_TRAFFICLIGHT')
    glb.PIN_OUT_K3_LAMP = db.get_pin_by_code('PIN_OUT_K3_LAMP')
    glb.PIN_OUT_K4_MODEM = db.get_pin_by_code('PIN_OUT_K4_MODEM')
    glb.PIN_IN_CABINET_OPEN_DOOR_BUTTON = db.get_pin_by_code('PIN_IN_CABINET_OPEN_DOOR_BUTTON')
    glb.PIN_IN_WIFI_BUTTON = db.get_pin_by_code('PIN_IN_WIFI_BUTTON')


@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({
        "version_app33": APP_VERSION, 
        "time": time.time(),
        "marker": '12'
    }), 200


if __name__ == '__main__':
    init()
    # app.run(host='0.0.0.0', port=5011)
    # debug=True включает и отладчик, и reloader
    
    print("!!!!!!!!!!!!!! NEW VERSION 3334 DEPLOYED VIA GITHUB ACTIONS !!!!!!!!!!!!!!")
    app.run(host='0.0.0.0', port=5011, debug=True)

    # app.run(
    #     host='0.0.0.0',
    #     port=5011,
    #     debug=True,
    #     ssl_context=('cert.pem', 'key.pem') # <-- Добавляем SSL-контекст
    # )

