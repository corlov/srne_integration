import time
import RepkaPi.GPIO as GPIO
import redis
import os
import psycopg2
from psycopg2 import sql
import psycopg2.extras


# Задача этого модуля все состояния по гпио в редис поместить

# https://repka-pi.ru/blog/post/45
# sudo apt-get install python3-dev python3-setuptools git
# git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git
# cd repkapigpiofs
# sudo python3 setup.py install

# print(GPIO.getboardmodel(), GPIO.VERSION, GPIO.RPI_INFO)


#FIXME: это названия ключей для нескольких микросервисов используются - нужно в БД или куда то еще определить
RK_WIFI_STATUS = 'wifi_status'
RK_WIFI_ON_REQ = 'wifi_activate_on_request'
RK_WIFI_OFF_REQ = 'wifi_activate_off_request'
RK_WIFI_TS = 'wifi_activate_ts'
RK_WIFI_ERROR = 'wifi_error_text'
RK_WIFI_ERROR_DETAILS = 'wifi_error_text_details'


PIN_OUT_K2_TRAFFICLIGHT = 22
PIN_OUT_K3_LAMP = 24
PIN_OUT_K4_MODEM = 26
PIN_IN_CABINET_OPEN_DOOR_BUTTON = 16
PIN_IN_WIFI_BUTTON = 18


PinsOut = [PIN_OUT_K2_TRAFFICLIGHT, PIN_OUT_K3_LAMP, PIN_OUT_K4_MODEM]
PinsIn = [PIN_IN_WIFI_BUTTON, PIN_IN_CABINET_OPEN_DOOR_BUTTON]


def init_pins():
    GPIO.setmode(GPIO.BOARD)

    for pin in PinsOut:
        GPIO.setup(pin, GPIO.OUT)

    # GPIO.PUD_UP = state (HIGH) when the button is not pressed
    GPIO.setup(PIN_IN_CABINET_OPEN_DOOR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.PUD_DOWN = state (HIGH) when the button is pressed
    GPIO.setup(PIN_IN_WIFI_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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



def event_log_add(descr, name, type, severity):
    # FIXME: try except
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("insert into device.event_log (event_type, event_name, description, severity) values (%s, %s, %s, %s)", (type, name, descr, severity, ))
        conn.commit()


def main():
    init_pins()

    REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    prev_opend_door_state = GPIO.input(PIN_IN_CABINET_OPEN_DOOR_BUTTON)
    prev_wifi_btn_state = GPIO.input(PIN_IN_WIFI_BUTTON)

    try:
        while True:
            # Small delay to debounce
            time.sleep(0.2)

            r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

            # обновляем значения в редисе по входным пинам
            for pin in PinsIn:
                redis_pin_name = f'GPIO.{pin}'
                state = GPIO.input(pin)
                print(f'{redis_pin_name}: {state}')
                if state == GPIO.LOW:
                    r.set(redis_pin_name, 0)
                else:
                    r.set(redis_pin_name, 1)

                if pin == PIN_IN_WIFI_BUTTON and state == GPIO.HIGH and prev_wifi_btn_state == GPIO.LOW:
                    r.set(RK_WIFI_ON_REQ, 1)
                    event_log_add('on', 'wifi button', 'EVENT', 'INFO')
                if pin == PIN_IN_WIFI_BUTTON and state == GPIO.LOW and prev_wifi_btn_state == GPIO.HIGH:
                    r.set(RK_WIFI_ON_REQ, 1)
                    event_log_add('off', 'wifi button', 'EVENT', 'INFO')

                if pin == PIN_IN_CABINET_OPEN_DOOR_BUTTON and state == GPIO.HIGH and prev_opend_door_state == GPIO.LOW:
                    event_log_add('Открыта дверь шкафа', 'дверь шкафа', 'EVENT', 'INFO')
                if pin == PIN_IN_CABINET_OPEN_DOOR_BUTTON and state == GPIO.LOW and prev_opend_door_state == GPIO.HIGH:
                    event_log_add('Закрыта дверь шкафа', 'дверь шкафа', 'EVENT', 'INFO')
                    
            prev_opend_door_state = GPIO.input(PIN_IN_CABINET_OPEN_DOOR_BUTTON)
            prev_wifi_btn_state = GPIO.input(PIN_IN_WIFI_BUTTON)

            print(time.time(), f'\n')

            # в зависмости от того что установлено в Редисе отправляем на устройство соотв. сигнал
            for pin in PinsOut:
                redis_pin_name = f'GPIO.{pin}'
                
                if r.exists(redis_pin_name):
                    state = r.get(f'GPIO.{pin}')
                    if int(state):
                        GPIO.output(pin, GPIO.HIGH)
                    else:
                        GPIO.output(pin, GPIO.LOW)
                    print(redis_pin_name, state)
    finally:
        GPIO.cleanup()

main()
