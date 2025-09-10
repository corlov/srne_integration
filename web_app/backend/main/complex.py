from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt
import datetime
import time
import json
import uuid
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
from gpio import gpio_bp
from decorators import auth_required

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gpio_bp, url_prefix='/gpio')



# журнал полученных параметров с контроллера СП
@app.route('/params_log', methods=['GET'])
@auth_required
def params_log():
    limit = request.args.get("limit", type=int)
    start_d, end_d = u.convert_dates(request.args.get("start_date"), request.args.get("end_date"))

    result = db.get_params_log(start_d, end_d, limit)
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })



# журнал того что во внутренней памяти самого контроллера СП лежит
@app.route('/controller_internal_log', methods=['GET'])
@auth_required
def controller_internal_log():
    limit = request.args.get("limit", type=int)
    start_d, end_d = u.convert_dates(request.args.get("start_date"), request.args.get("end_date"))

    result = db.get_controller_internal_log(start_d, end_d, limit)
    return jsonify({
        'success': True,
        'data': result,
        'total': len(result)
    })



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




@app.route("/api/change_time_source", methods=["GET"])
def change_time_source():
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                MAX(CASE WHEN param = 'time_source' THEN value END) as src,
                MAX(CASE WHEN param = 'time_source_addr' THEN value END) as addr
            FROM device.complex_settings
            WHERE param IN ('time_source', 'time_source_addr')
        """)
        rs = cur.fetchone()
        if not rs:
            return None, None
        src = rs["src"]
        addr = rs["addr"]

        print(src, addr)
        if src == 'NTP' and addr:
            print('source: NTP')
            os.system('systemctl stop chronyd')            
            os.system("sed -i '1i\server " + addr + " iburst prefer' /etc/chrony/chrony.conf")
            os.system('systemctl start chronyd')
        else:
            print('source: RTC')
            os.system('systemctl stop chronyd')

    return 'ok'


   

@app.route("/api/settings", methods=["GET"])
def list_settings():
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select id, descr as name, value, type, options, param from device.complex_settings cs order by ui_field_order")        

        rows = cur.fetchall()
        # options stored as JSON in DB; psycopg2 will map to Python list/dict
        return jsonify(rows)



@app.route("/api/settings/<int:setting_id>", methods=["PUT"])
def update_setting(setting_id):
    data = request.get_json() or {}
    if "value" not in data:
        return abort(400, "Missing value")
    new_value = data["value"]

    # fetch setting for validation
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, descr as name, type, options FROM device.complex_settings WHERE id = %s", (setting_id,))
        s = cur.fetchone()
        if not s:
            return abort(404)
        t = s["type"]
        opts = s.get("options")

        # Simple validation/conversion
        if t == "boolean":
            if not isinstance(new_value, bool):
                # allow strings 'true'/'false'
                if isinstance(new_value, str) and new_value.lower() in ("true","false"):
                    new_value = new_value.lower() == "true"
                else:
                    return abort(400, "Invalid boolean")
            store_value = "true" if new_value else "false"
        elif t == "select":
            if opts is None:
                return abort(500, "No options defined")
            if new_value not in opts:
                return abort(400, "Invalid option")
            store_value = str(new_value)
        else:  # string or default
            store_value = str(new_value)

        cur.execute("UPDATE device.complex_settings SET value = %s WHERE id = %s", (store_value, setting_id))
        conn.commit()
        return jsonify({"ok": True})




@app.route('/dynamic_data_events/<device_id>')
def events(device_id):
    def generate_events():
        while True:
            data_dict = im.redis_read_json(im.RK_TELEMETRY, device_id)
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(5)
            
    #token = request.headers.get('Authorization')
    token = request.args.get('Authorization')
    
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
        print("Hello, ", data['username'])
        return Response(generate_events(), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')
            
    #return Response(generate_events(), content_type='text/event-stream')






@app.route('/clear_events_log')
def clear_events_log():
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("truncate device.event_log")
        conn.commit()
    return jsonify(message='OK')



@app.route('/clear_params_log')
def clear_params_log(clear_events_log):
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("truncate device.dynamic_information")
        conn.commit()
    return jsonify(message='OK')








def cmd_body(command_name):
    now = datetime.datetime.now()
    cmd = {}
    #TODO: авторизацию на распбери надо сделать хотя бы basic
    cmd['user'] = 'admin'
    cmd['command'] = command_name
    cmd['created_at'] = str(now.timestamp())
    cmd['uuid'] = str(uuid.uuid4())
    return cmd



@app.route('/load_control', methods=['GET'])
def load_control():
    mode = request.args.get('mode')
    device_id = request.args.get('device_id')
    db.event_log_add(f'{mode}', 'UI lamp on off', 'EVENT', 'DEBUG')
    cmd = cmd_body('control_load_on_off')
    cmd['value'] = mode
    im.redis_set('command' + str(device_id), json.dumps(cmd))
    return 'OK'



@app.route('/wifi', methods=['GET'])
def wifi_set():
    try:
        state = request.args.get('state')        
        db.event_log_add(f'{state}', 'wifi', 'EVENT', 'INFO')

        if state == 'on':
            im.redis_set(im.RK_WIFI_ON_REQ, 1)

        if state == 'off':
            im.redis_set(im.RK_WIFI_OFF_REQ, 1)

        return 'ok'
    except jwt.ExpiredSignatureError:
        print('Token has expired!')
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        print('Invalid token!')
        return jsonify(message='Invalid token!')


@app.route('/wifi_get', methods=['GET'])
def wifi_get():
    try:
        return jsonify({
            'mode': im.redis_read_v(im.RK_WIFI_STATUS).decode('utf-8'), 
            'error_text': im.redis_read_v(im.RK_WIFI_ERROR).decode('utf-8'),
            'error_details': im.redis_read_v(im.RK_WIFI_ERROR_DETAILS).decode('utf-8'),
        })
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')



@app.route('/wifi_status')
def events_wifi_status():
    def generate_events():
        while True:
            data_dict = {
                'mode': im.redis_read_v(im.RK_WIFI_STATUS).decode('utf-8'), 
                'error_text': im.redis_read_v(im.RK_WIFI_ERROR).decode('utf-8'),
                'error_details': im.redis_read_v(im.RK_WIFI_ERROR_DETAILS).decode('utf-8'),
            }
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(5)

    token = request.args.get('Authorization')    
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
        return Response(generate_events(), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')





def get_complex_settings():
    connection_params = {
        'host': 'localhost',
        'database': 'solar_controller_telemetry',
        'user': 'postgres',
        'password': 'gen_postgress_password',
        'port': '5432'
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        query = sql.SQL("SELECT param, value FROM solar_controller_telemetry.device.complex_settings order by ui_field_order")
        cursor.execute(query)        
        rows = cursor.fetchall()
        result_dict = {key: value for key, value in rows}
        
        return result_dict

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return {}


@app.route('/update_status/<device_id>')
def update_status(device_id):
    print(f'================ update_status ========')
    def generate_update_events(device_id):
        while True:            
            dict_wifi = {
                'mode': im.redis_read_v(im.RK_WIFI_STATUS).decode('utf-8'), 
                'error_text': im.redis_read_v(im.RK_WIFI_ERROR).decode('utf-8'),
                'error_details': im.redis_read_v(im.RK_WIFI_ERROR_DETAILS).decode('utf-8'),
            }

            sys_list = im.redis_read_json(im.RK_SYS_INFO, device_id)
            dict_system_info = {}
            for s in sys_list:
                for key, value in s.items():
                    if key != 'unit':
                        dict_system_info[key] = value

            data_dict = {
                'wifi': dict_wifi,
                'device_settings': im.redis_read_json(im.RK_SETTINGS, device_id),
                'device_system_info': dict_system_info,
                'complex_settings': get_complex_settings()
            }

            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(2)

    token = request.args.get('Authorization')
    if not token:
        return jsonify(message='Token is missing!')
    print(f'Token: {token}')
    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
        #device_id = request.args.get('deviceId')
        print(f'EVENT: init, dev_id: {device_id}')
        return Response(generate_update_events(device_id), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')



@app.route("/api/controller-temp")
def controller_temp():
    """
    Query params:
      - range: e.g. '7d' (default) or '24h'
      - downsample: integer minutes to bucket points (optional, e.g. 15)
      - limit: max raw points when no downsample (optional)
    Returns JSON array: [{ "x": ISO8601, "y": int }, ...]
    """
    rng = request.args.get("range", "7d")
    downsample = request.args.get("downsample", type=int)
    limit = request.args.get("limit", type=int, default=10000)

    # parse range
    now = datetime.datetime.now(datetime.timezone.utc)
    if rng.endswith("d"):
        hours = int(rng[:-1]) * 24
    elif rng.endswith("h"):
        hours = int(rng[:-1])
    else:
        hours = 24 * 7
    start = now - datetime.timedelta(hours=hours)

    
    with db.get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        if downsample and downsample > 0:
            # bucket by downsample minutes using date_trunc on minutes and integer division
            sql = """
                SELECT
                to_char(date_trunc('minute', di.created_at AT TIME ZONE 'UTC')
                        + make_interval(mins => (floor(date_part('minute', di.created_at AT TIME ZONE 'UTC') / %s) * %s)),
                        'YYYY-MM-DD"T"HH24:MI:SS"Z"') AS ts,
                AVG((di.payload -> 'controller' ->> 'temperature')::numeric) AS avg_temp
                FROM device.dynamic_information di
                WHERE di.payload ? 'controller'
                AND (di.payload -> 'controller') ? 'temperature'
                AND di.created_at >= %s
                GROUP BY ts
                ORDER BY ts;
            """
            cur.execute(sql, (downsample, downsample, start))
            rows = cur.fetchall()
            data = rows
        else:
            sql = """
                	select 
                        *
                    from
                    (
                    SELECT 
                            (di.created_at AT TIME ZONE 'UTC')::date AS ts,
                            avg((di.payload -> 'controller' ->> 'temperature')::int) AS controller_temperature,
                            avg((di.payload -> 'battery' ->> 'temperature')::int) AS battery_temperature,
                            avg((di.payload -> 'battery' ->> 'volts')::float) AS battery_volts
                    FROM device.dynamic_information di
                    WHERE 
                        di.payload ? 'controller' 
                        AND (di.payload -> 'controller') ? 'temperature'
                        AND di.payload ? 'battery' 
                        AND (di.payload -> 'battery') ? 'temperature'
                        AND (di.payload -> 'battery') ? 'volts'
                    group by ts	
                    ORDER BY ts
                    ) as t1
                    join
                    (
                    select
                        h.actual_date::date as ts,
                        avg((h.payload->'maxBatteryVoltage')::int) as maxv,
                        avg((h.payload->'currentDayMinBatteryVoltage')::int) as minv
                    from device.history h
                    group by h.actual_date::date 	
                    ORDER BY h.actual_date::date
                    ) as t2 on t1.ts = t2.ts
            """
            cur.execute(sql)
            rows = cur.fetchall()
            controller_temperature = [{"x": r["ts"], "y": r["controller_temperature"]} for r in rows]
            battery_temperature = [{"x": r["ts"], "y": r["battery_temperature"]} for r in rows]
            battery_volts = [{"x": r["ts"], "y": r["battery_volts"]} for r in rows]
            maxv = [{"x": r["ts"], "y": r["maxv"]} for r in rows]
            minv = [{"x": r["ts"], "y": r["minv"]} for r in rows]
            data = {
                'controller_temperature': controller_temperature,
                'battery_temperature': battery_temperature,
                'battery_volts': battery_volts,
                'maxv': maxv,
                'minv': minv
            }

        return jsonify(data)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)

