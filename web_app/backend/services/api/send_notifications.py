from flask import Blueprint
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


notify_bp = Blueprint('notify', __name__)



@notify_bp.route('/dynamic_data_events/<device_id>')
def events(device_id):
    def generate_update_dynamic_data_events():
        while True:
            data_dict = im.redis_read_json(im.RK_TELEMETRY, device_id)
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(glb.SSE_UPDATE_DYNAMIC_DATA_TIMEOUT)
    
    if not device_id or int(device_id) > 4:
        return jsonify({"error": "Invalid device_id"}), 400

    token = request.args.get('Authorization')
    if not token:
        return jsonify(message='Token is missing!')
    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
        return Response(generate_update_dynamic_data_events(), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')



@notify_bp.route('/complex_events/<device_id>')
def update_status(device_id):
    def generate_update_complex_events(device_id):
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
                'complex_settings': db.get_complex_param_val_settings()
            }
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(glb.SSE_UPDATE_COMPLEX_STATUS_TIMEOUT)

    token = request.args.get('Authorization')
    if not token:
        return jsonify(message='Token is missing!')    
    try:
        data = jwt.decode(token, glb.SECRET_KEY, algorithms=["HS256"])
        return Response(generate_update_complex_events(device_id), content_type='text/event-stream')
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired!')
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token!')
