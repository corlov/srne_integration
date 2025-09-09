#
# Испольняет режим работы светофора заданый
#
import time
import RepkaPi.GPIO as GPIO
import redis
import os
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import json

REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
RK_TELEMETRY = 'telemetry'
# FIXME: параметр контейнера 
device_id = 2
MODE_1 = "режим 1 (1Гц, 500мс)"
MODE_2 = "режим 2 (1Гц, 100мс)"
MODE_3 = "режим 3 (алгоритм)"
MODE_4 = "режим 4 (откл.)"
PIN_OUT_K2_TRAFFICLIGHT = 22
HI_VOLTAGE = 11.2
LOW_VOLTAGE = 10.2

#FIXME: реконнект сделать к объекту если соединение утеряно
r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

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



# ERROR EVENT
# DEBUG INFO WARNING ERROR
def event_log_add(descr, name, type, severity):
    # FIXME: try except
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("insert into device.event_log (event_type, event_name, description, severity) values (%s, %s, %s, %s)", (type, name, descr, severity, ))
        conn.commit()



def get_actual_mode():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select value from device.complex_settings cs where param = 'trafficlight_work_mode'")
        s = cur.fetchone()
        if not s:
            return None
        return s["value"]



def redis_read(key_name, device_id="", additonal_params=""):
    key = key_name + str(device_id) + additonal_params
    payload = ''
    if r.exists(key):
        payload = r.get(key)
        return json.loads(payload)
    return ''



def economy_blink():
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
    time.sleep(0.9)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 1)
    time.sleep(0.1)



def normal_blink():
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
    time.sleep(0.5)
    r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 1)
    time.sleep(0.5)



def main():
    k = 0
    mode = get_actual_mode()
    data = redis_read(RK_TELEMETRY, device_id)
    voltage = float(data['battery']['volts'])
    hold_prev_voltage = False

    current_mode = mode

    while True:
        k += 1
        time.sleep(0.001)
        if k > 10:
            mode = get_actual_mode()
            print(mode)
            k = 0
            if current_mode != mode:
                event_log_add(f'Смена режима {current_mode} -> {mode}', 'trafficlight control daemon', 'EVENT', 'WARNING')

        # изменяем режим только если не включен спец. режим гистерезиса, когда нужно помнить из какого напряжения попали в текущее
        if not hold_prev_voltage:
            prev_voltage = voltage
        data = redis_read(RK_TELEMETRY, device_id)
        voltage = float(data['battery']['volts'])

        if mode == MODE_1:
            normal_blink()
        elif mode == MODE_2:
            economy_blink()
        elif mode == MODE_3:
            if voltage > HI_VOLTAGE:
                normal_blink()
                hold_prev_voltage = False
            elif voltage < LOW_VOLTAGE:
                economy_blink()
                hold_prev_voltage = False
            else:
                # зависит от того с какой стороны попали в диапазон - гистерезис
                # если было меньше 10.8 и зашло в диапазон, но 2, если 
                # было больше 11.2 и попало в диапазон, то 1
                if not hold_prev_voltage:
                    hold_prev_voltage = True
                    event_log_add(f'Режим гистерезиса', 'trafficlight control daemon', 'EVENT', 'WARNING')

                if prev_voltage < LOW_VOLTAGE:
                    economy_blink()
                elif prev_voltage < LOW_VOLTAGE:
                    normal_blink()
                else:
                    economy_blink()
        elif mode == MODE_4:
            r.set(f'GPIO.{PIN_OUT_K2_TRAFFICLIGHT}', 0)
        else:
            event_log_add(f'Нераспознаный режим {mode}', 'trafficlight control daemon', 'ERROR', 'ERROR')

        current_mode = mode



main()
