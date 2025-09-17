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



def main():
    init()

    k = 0
    mode = db.get_actual_mode()
    data = redis_read(glb.RK_TELEMETRY, glb.DEVICE_ID)
    voltage = float(data['battery']['volts'])
    hold_prev_voltage = False

    current_mode = mode

    while True:
        k += 1
        time.sleep(0.001)
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
