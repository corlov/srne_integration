#!/usr/bin/python3

import time
import RepkaPi.GPIO as GPIO
import redis
import os
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import logging

import utils as u
import glb_consts as glb
import db


# Задача этого модуля все состояния по гпио в редис поместить

# https://repka-pi.ru/blog/post/45
# sudo apt-get install python3-dev python3-setuptools git
# git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git
# cd repkapigpiofs
# sudo python3 setup.py install


PIN_OUT_K2_TRAFFICLIGHT = None
PIN_OUT_K3_LAMP = None
PIN_OUT_K4_MODEM = None
PIN_IN_CABINET_OPEN_DOOR_BUTTON = None
PIN_IN_WIFI_BUTTON = None

PinsOut = []
PinsIn = []
output_pins_state = {}



def init_pins():
    global PIN_OUT_K2_TRAFFICLIGHT, PIN_OUT_K3_LAMP, PIN_OUT_K4_MODEM, PIN_IN_CABINET_OPEN_DOOR_BUTTON, PIN_IN_WIFI_BUTTON
    global PinsOut
    global PinsIn
    global output_pins_state

    PIN_OUT_K2_TRAFFICLIGHT = db.get_pin_by_code('PIN_OUT_K2_TRAFFICLIGHT')
    PIN_OUT_K3_LAMP = db.get_pin_by_code('PIN_OUT_K3_LAMP')
    PIN_OUT_K4_MODEM = db.get_pin_by_code('PIN_OUT_K4_MODEM')
    PIN_IN_CABINET_OPEN_DOOR_BUTTON = db.get_pin_by_code('PIN_IN_CABINET_OPEN_DOOR_BUTTON')
    PIN_IN_WIFI_BUTTON = db.get_pin_by_code('PIN_IN_WIFI_BUTTON')

    PinsOut = [PIN_OUT_K2_TRAFFICLIGHT, PIN_OUT_K3_LAMP, PIN_OUT_K4_MODEM]
    PinsIn = [PIN_IN_WIFI_BUTTON, PIN_IN_CABINET_OPEN_DOOR_BUTTON]

    output_pins_state = {
        PIN_OUT_K2_TRAFFICLIGHT: GPIO.LOW,
        PIN_OUT_K3_LAMP: GPIO.LOW,
        PIN_OUT_K4_MODEM: GPIO.LOW
    }

    GPIO.setmode(GPIO.BOARD)

    for pin in PinsOut:
        GPIO.setup(pin, GPIO.OUT)

    # GPIO.PUD_UP = state (HIGH) when the button is not pressed
    GPIO.setup(PIN_IN_CABINET_OPEN_DOOR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.PUD_DOWN = state (HIGH) when the button is pressed
    GPIO.setup(PIN_IN_WIFI_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    db.event_log_add('Инициализация пинов', 'gpio', 'EVENT', 'DEBUG')



def init():
    if not os.path.exists(u.LOG_PATH):
        os.makedirs(u.LOG_PATH)    

    log_file = os.path.join(u.LOG_PATH, u.MAIN_LOG_FILE)
    if os.path.exists(log_file):
        size_limit = 1024*1024*30  # 30Mb
        file_size = os.path.getsize(log_file)
        if file_size > size_limit:
            try:
                os.remove(log_file)
            except:
                print(f"cant remove the log file")
    
    logging.basicConfig(filename=log_file, force=True, level=logging.DEBUG, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    glb.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    glb.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    glb.PG_CONNECT_PARAMS = { 
        'dbname': os.getenv('DB_NAME', 'solar_controller_telemetry'), 
        'user': os.getenv('DB_USER', 'postgres'), 
        'password': os.getenv('DB_PASSWORD', 'gen_postgress_password'), 
        'host': os.getenv('DB_HOST', 'localhost'), 
        'port': int(os.getenv('DB_PORT', 5432)), 
    }

    init_pins()



def main():
    init()

    u.logmsg('Started v.1.0.0')
    u.logmsg(f'model: {GPIO.getboardmodel()}, ver: {GPIO.VERSION}, info: {GPIO.RPI_INFO}')
    

    prev_opend_door_state = GPIO.input(PIN_IN_CABINET_OPEN_DOOR_BUTTON)
    prev_wifi_btn_state = GPIO.input(PIN_IN_WIFI_BUTTON)

    prev_time = time.time()
    try:
        k = 0
        while True:
            if k > 20:
                k = 0
            k += 1
            # Small delay to debounce
            time.sleep(0.2)

            if time.time() - prev_time > glb.HEARTBEAT_UPD_TIMEOUT:
                db.event_log_add('Тест связи', 'gpio', 'EVENT', 'DEBUG')
                u.logmsg(f'tick')
                prev_time = time.time()

            r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
            r.set(glb.RK_HCHK, time.time())

            # обновляем значения в редисе по входным пинам
            for pin in PinsIn:
                redis_pin_name = f'GPIO.{pin}'
                state = GPIO.input(pin)
                if k > 20:
                    u.logmsg(f'in {redis_pin_name}: {state}')

                if state == GPIO.LOW:
                    r.set(redis_pin_name, 0)
                else:
                    r.set(redis_pin_name, 1)

                if pin == PIN_IN_WIFI_BUTTON and state == GPIO.HIGH and prev_wifi_btn_state == GPIO.LOW:
                    r.set(glb.RK_WIFI_ON_REQ, 1)
                    db.event_log_add('on', 'gpio: wifi button', 'EVENT', 'INFO')
                if pin == PIN_IN_WIFI_BUTTON and state == GPIO.LOW and prev_wifi_btn_state == GPIO.HIGH:
                    r.set(glb.RK_WIFI_ON_REQ, 1)
                    db.event_log_add('off', 'gpio: wifi button', 'EVENT', 'INFO')

                if pin == PIN_IN_CABINET_OPEN_DOOR_BUTTON and state == GPIO.HIGH and prev_opend_door_state == GPIO.LOW:
                    db.event_log_add('Открыта дверь шкафа', 'gpio: дверь шкафа', 'EVENT', 'INFO')
                if pin == PIN_IN_CABINET_OPEN_DOOR_BUTTON and state == GPIO.LOW and prev_opend_door_state == GPIO.HIGH:
                    db.event_log_add('Закрыта дверь шкафа', 'gpio: дверь шкафа', 'EVENT', 'INFO')
                    
            prev_opend_door_state = GPIO.input(PIN_IN_CABINET_OPEN_DOOR_BUTTON)
            prev_wifi_btn_state = GPIO.input(PIN_IN_WIFI_BUTTON)

            if k > 20:
                u.logmsg(f'{time.time()}\n\n')

            # в зависмости от того что установлено в Редисе отправляем на устройство соотв. сигнал
            for pin in PinsOut:
                redis_pin_name = f'GPIO.{pin}'
                
                if r.exists(redis_pin_name):
                    state = r.get(f'GPIO.{pin}')

                    if output_pins_state[pin] != state:
                        #db.event_log_add(f'Смена состояния pin({pin}) {output_pins_state[pin]} -> {state}', 'gpio', 'EVENT', 'DEBUG')
                        output_pins_state[pin] = state

                    if int(state):
                        GPIO.output(pin, GPIO.HIGH)
                    else:
                        GPIO.output(pin, GPIO.LOW)
                    if k > 20:
                        u.logmsg(f'out {redis_pin_name}: {state}')
    finally:
        GPIO.cleanup()

main()
