from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt
import datetime
import time
import redis
import json
import uuid
import os
import bcrypt
import psycopg2
from psycopg2 import sql
import psycopg2.extras



app = Flask(__name__)
CORS(app)
SECRET_KEY = 'uw3cok92adxmzpf35_secret_key_value_12082025'

# TODO: загрузить из хранилища информацию о пользователях
users = [
        # 123
        {'username': 'user', 'hashed_password': b'$2b$12$VsKwKBwbwZF3.pdBVUAjZu4/h1IAVxIWltoY5ccxtkyU2vxq9xIn.'},
        # 12345
        {'username': 'admin', 'hashed_password': b'$2b$12$1iUzgD74nAmOJS49OFdjqeUqNcnRYy/qHjuIPAPZUCeQILz1Z56S6'},
]  


REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

RK_TELEMETRY = 'telemetry'
RK_SYS_INFO = 'system_information'
RK_SETTINGS = 'eeprom_parameter_setting'
RK_COMMAND = 'command'
RK_HISTORY = 'history'
RK_COMMAND_RESPONSE = 'commands_responses'


def redis_read(key_name, device_id, additonal_params=""):
    r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
    
    key = key_name + str(device_id) + additonal_params
    payload = ''
    if r.exists(key):
        payload = r.get(key)
        return json.loads(payload)

    return ''
    
    
@app.route('/dynamic_data', methods=['GET'])
def dynamic_data_get():    
    device_id = request.args.get('deviceId')
    return redis_read(RK_TELEMETRY, device_id)


@app.route('/system_info', methods=['GET'])
def system_info():
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Hello, ", data['username'])
        
        device_id = request.args.get('deviceId')

        sys_list = redis_read(RK_SYS_INFO, device_id)
        res_hash = {}
        for s in sys_list:
            for key, value in s.items():
                if key != 'unit':
                    res_hash[key] = value
        print(res_hash)
        return res_hash
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')


# настройки контроллера СП
@app.route('/settings', methods=['GET'])
def settings():
    token = request.headers.get('Authorization')
        
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Hello, ", data['username'])
        
        device_id = request.args.get('deviceId')
        return redis_read(RK_SETTINGS, device_id)    
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')
            

# настройки всего комплекса
@app.route('/complex_settings', methods=['GET'])
def complex_settings():
    # FIXME: в настройки пароли убрать
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
        query = sql.SQL("SELECT param, value FROM solar_controller_telemetry.device.complex_settings")        
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


def row_to_dict(row):
    """Конвертирует строку из БД в словарь"""
    if row is None:
        return None
    return {key: value for key, value in row.items()}


def get_conn():
    # FIXME: в настройки пароли убрать
    connection_params = {
        'host': 'localhost',
        'database': 'solar_controller_telemetry',
        'user': 'postgres',
        'password': 'gen_postgress_password',
        'port': '5432'
    }

    return psycopg2.connect(**connection_params)
        
@app.route('/params_log', methods=['GET'])
def params_log():
    # FIXME: в настройки пароли убрать
    connection_params = {
        'host': 'localhost',
        'database': 'solar_controller_telemetry',
        'user': 'postgres',
        'password': 'gen_postgress_password',
        'port': '5432'
    }

    # FIXME: non secure!
    start_d = request.args.get("start_date")
    end_d = request.args.get("end_date")
    limit = request.args.get("limit", type=int)
    
    
    print('2', limit, start_d, end_d)
    
    if not start_d:
        start_d = datetime.datetime.now().strftime('%Y-%m-%d')

    if not end_d:
        end_d = datetime.datetime.now().strftime('%Y-%m-%d')

    # Build timestamp strings
    start_d = f"{start_d} 00:00:00"
    end_d   = f"{end_d} 23:59:59"

    
    print('3', limit, start_d, end_d)
    
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("""
            select
	            to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at,
	            payload->'panels'->>'volts' as panel_volts,
	            payload->'battery'->>'volts' as battery_volts,
	            payload->'battery'->>'stateOfCharge' as battery_stateOfCharge,
	            payload->'load'->>'amps' as load_amps,
	            payload->'load'->>'dailyPower' as load_dailyPower,    
	            payload->'controller'->>'chargingMode' as controller_chargingMode,
	            payload->'load'->>'state' as load_state,
	            payload->'controller'->>'temperature' as controller_temperature
            from solar_controller_telemetry.device.dynamic_information di
            where
                created_at between %(start_d)s and %(end_d)s
            order by created_at desc 
            limit %(limit)s;
        """, {"limit": limit, "start_d": start_d, "end_d": end_d})        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()            
        result = []
        for row in rows:
            item = {}
            for i, column in enumerate(columns):
                item[column] = row[i]
            result.append(item)

        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        })


    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return {}



@app.route("/api/settings", methods=["GET"])
def list_settings():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select id, descr as name, value, type, options from device.complex_settings cs order by id")

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
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
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
            print('event')
            data_dict = redis_read(RK_TELEMETRY, device_id)
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(5)
            
    #token = request.headers.get('Authorization')
    token = request.args.get('Authorization')
    
    if not token:
        return jsonify(message='Token is missing!')

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Hello, ", data['username'])
        return Response(generate_events(), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')
            
    #return Response(generate_events(), content_type='text/event-stream')



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    username = data['username']
    password = data['password'].encode('utf-8')

    user = next((u for u in users if u['username'] == username), None)

    if user and bcrypt.checkpw(password, user['hashed_password']):
       token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, SECRET_KEY)
       return jsonify(token=token)
    return jsonify(message='Invalid credentials')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)
    
    
