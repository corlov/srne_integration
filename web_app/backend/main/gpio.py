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
# local modules:
import common.db as db
import common.glb_consts as glb
import common.inmemory as im
import common.utils as u


gpio_bp = Blueprint('gpio', __name__)



@gpio_bp.route('/state')
def events_gpio():
    def generate_events():
        while True:
            data_dict = {
                'k2': im.redis_read_json(f'GPIO.{glb.PIN_OUT_K2_TRAFFICLIGHT}'),
                'k3': im.redis_read_json(f'GPIO.{glb.PIN_OUT_K3_LAMP}'),
                'k4': im.redis_read_json(f'GPIO.{glb.PIN_OUT_K4_MODEM}'),
                'k4': im.redis_read_json(f'GPIO.{glb.PIN_OUT_K4_MODEM}'),
                'open_door_alarm': im.redis_read_json(f'GPIO.{glb.PIN_IN_CABINET_OPEN_DOOR_BUTTON}'),
                'wifi_button_is_pressed': im.redis_read_json(f'GPIO.{glb.PIN_IN_WIFI_BUTTON}') 
            }
            yield f"data: {json.dumps(data_dict)}\n\n"
            time.sleep(glb.SSE_UPDATE_GPIO_TIMEOUT)

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




@gpio_bp.route('/set_pin', methods=['GET'])
def gpio_set_pin():
    pin_alias = request.args.get('pin')

    pin = None
    if pin_alias == 'PIN_OUT_K2_TRAFFICLIGHT':
        pin = glb.PIN_OUT_K2_TRAFFICLIGHT
    if pin_alias == 'PIN_OUT_K3_LAMP':
        pin = glb.PIN_OUT_K3_LAMP
    if pin_alias == 'PIN_OUT_K4_MODEM':
        pin = glb.PIN_OUT_K4_MODEM

    if pin:
        state = im.redis_get(f'GPIO.{pin}')
        if int(state):
            im.redis_set(f'GPIO.{pin}', 0)
            print(f'GPIO.{pin} 0')
        else:
            im.redis_set(f'GPIO.{pin}', 1)
            print(f'GPIO.{pin} 1')
        return 'OK'
    else:
        return jsonify({"error": "Invalid pin number"}), 400
