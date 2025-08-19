from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import datetime
import time
import redis
import json
from datetime import datetime
import uuid
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
SECRET_KEY = 'your_secret_key'  # Change this to a strong secret key

# In-memory user storage
users = []  


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



@app.route('/dynamic_data_events')
def events():
    def generate_events():
        while True:
            print('event')
            data_dict = redis_read(RK_TELEMETRY, 2)
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(5)
            
    return Response(generate_events(), content_type='text/event-stream')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)
    
    
