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
    
    
