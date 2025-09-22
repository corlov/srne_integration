#!/usr/bin/python3

#
# Испольняет режим работы светофора заданый
#
import time
import redis
import json
import os

import db
import glb_consts as glb


PIN_OUT_K2_TRAFFICLIGHT = None



def redis_read(key_name, device_id="", additonal_params=""):
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    key = key_name + str(glb.DEVICE_ID) + additonal_params
    payload = ''
    if r.exists(key):
        payload = r.get(key)
        return json.loads(payload)
    return ''



def economy_blink():
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
    time.sleep(0.9)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 1)
    time.sleep(0.1)



def normal_blink():
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
    time.sleep(0.5)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 1)
    time.sleep(0.5)



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
    global PIN_OUT_K2_TRAFFICLIGHT

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

    PIN_OUT_K2_TRAFFICLIGHT = db.get_pin_by_code('PIN_OUT_K2_TRAFFICLIGHT')

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
        logmsg('started')



def main():
    init()

    k = 0
    mode = db.get_actual_mode()
    data = redis_read(glb.RK_TELEMETRY, glb.DEVICE_ID)
    voltage = float(data['battery']['volts'])
    hold_prev_voltage = False

    current_mode = mode
    prev_time = time.time()

    while True:
        k += 1
        time.sleep(0.001)

        if time.time() - prev_time > 60:
            logmsg('tick')
            prev_time = time.time()

        if k > 10:
            mode = db.get_actual_mode()
            print(mode)
            k = 0
            if current_mode != mode:
                db.event_log_add(f'Смена режима {current_mode} -> {mode}', 'trafficlight control daemon', 'EVENT', 'WARNING')

        # изменяем режим только если не включен спец. режим гистерезиса, когда нужно помнить из какого напряжения попали в текущее
        if not hold_prev_voltage:
            prev_voltage = voltage
        data = redis_read(glb.RK_TELEMETRY, glb.DEVICE_ID)
        voltage = float(data['battery']['volts'])

        if mode == glb.MODE_1:
            normal_blink()
        elif mode == glb.MODE_2:
            economy_blink()
        elif mode == glb.MODE_3:
            if voltage > glb.HI_VOLTAGE:
                normal_blink()
                hold_prev_voltage = False
            elif voltage < glb.LOW_VOLTAGE:
                economy_blink()
                hold_prev_voltage = False
            else:
                # зависит от того с какой стороны попали в диапазон - гистерезис
                # если было меньше 10.8 и зашло в диапазон, но 2, если 
                # было больше 11.2 и попало в диапазон, то 1
                if not hold_prev_voltage:
                    hold_prev_voltage = True
                    db.event_log_add(f'Режим гистерезиса', 'trafficlight control daemon', 'EVENT', 'WARNING')

                if prev_voltage < LOW_VOLTAGE:
                    economy_blink()
                elif prev_voltage < LOW_VOLTAGE:
                    normal_blink()
                else:
                    economy_blink()
        elif mode == glb.MODE_4:
            r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
        else:
            db.event_log_add(f'Нераспознаный режим {mode}', 'trafficlight control daemon', 'ERROR', 'ERROR')

        current_mode = mode



main()
