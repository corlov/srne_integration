#!/usr/bin/python3

#
# Испольняет режим работы светофора заданый
#
import time
import redis
import os
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import json
import datetime
import uuid

import db
import glb_consts as glb


PIN_OUT_K3_LAMP = None


def cmd_body(command_name):
    now = datetime.datetime.now()
    cmd = {}
    #TODO: авторизацию на распбери надо сделать хотя бы basic
    cmd['user'] = 'admin'
    cmd['command'] = command_name
    cmd['created_at'] = str(now.timestamp())
    cmd['uuid'] = str(uuid.uuid4())
    return cmd



def load_control(on_off):
    cmd = cmd_body('control_load_on_off')
    cmd['value'] = on_off
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set('command' + str(glb.DEVICE_ID), json.dumps(cmd))



def set_working_mode(mode):
    if mode >= 0x00 and mode <= 0x11:
        cmd = cmd_body('set_load_working_mode')
        cmd['value'] = mode
        r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
        r.set('command' + str(glb.DEVICE_ID), json.dumps(cmd))
    else:
        db.event_log_add(f'Нераспознаный режим работы контроллера СП {mode}', 'lamp control daemon', 'ERROR', 'ERROR')
        


def apply_mode(mode_complex, mode_controller):
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    if mode_complex == glb.MODE_1:
        set_working_mode(mode_controller)
        r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 1)
    elif mode_complex == glb.MODE_2:
        r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 0)
        set_working_mode(15)
        load_control(0)
    elif mode_complex == glb.MODE_3:
        r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 1)
        set_working_mode(15)
        load_control(1)
    else:
        db.event_log_add(f'Нераспознаный режим {mode_complex}', 'lamp control daemon', 'ERROR', 'ERROR')


LOG_PATH = 'logs'
MAIN_LOG_FILE = 'app.log'


def logmsg(message, level="INFO"): 
    from datetime import datetime

    log_file = os.path.join(LOG_PATH, MAIN_LOG_FILE)
    if os.path.exists(log_file):
        size_limit = 1024*1024*30  # 30Mb
        file_size = os.path.getsize(log_file)
        if file_size > size_limit:
            try:
                os.remove(log_file)
            except:
                print(f"cant remove the log file")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level.upper()}]: {message}"
    print(log_entry)    
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')



def init():
    global PIN_OUT_K3_LAMP

    glb.DEVICE_ID = int(os.getenv('DEVICE_ID', 2))
    glb.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    glb.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    glb.PG_CONNECT_PARAMS = { 
        'dbname': os.getenv('DB_NAME', 'solar_controller_telemetry'), 
        'user': os.getenv('DB_USER', 'postgres'), 
        'password': os.getenv('DB_PASSWORD', 'gen_postgress_password'), 
        'host': os.getenv('DB_HOST', 'localhost'), 
        'port': int(os.getenv('DB_PORT', 5432)), 
    }

    PIN_OUT_K3_LAMP = db.get_pin_by_code('PIN_OUT_K3_LAMP')

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
        logmsg('started v.1.0.0')



def main():
    init()

    mode_complex, mode_controller = db.get_actual_mode()
    apply_mode(mode_complex, mode_controller)
    current_mode = mode_complex
    prev_time = time.time()
    while True:
        time.sleep(1)

        if time.time() - prev_time > 60:
            logmsg('tick')
            prev_time = time.time()

        mode_complex, mode_controller = db.get_actual_mode()
        print(mode_complex, mode_controller)
        if current_mode != mode_complex:
            db.event_log_add(f'Смена режима {current_mode} -> {mode_complex}', 'lamp control daemon', 'EVENT', 'WARNING')
            apply_mode(mode_complex, mode_controller)

        current_mode = mode_complex


main()

