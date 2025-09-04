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
import datetime
import uuid

REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
RK_TELEMETRY = 'telemetry'
# FIXME: параметр контейнера 
device_id = 2
MODE_1 = "режим"
MODE_2 = "откл."
MODE_3 = "вкл."
PIN_OUT_K3_LAMP = 24

controller_modes_dict = {
    "контроль включения/выключения нагрузки": 0,
    "выкл. через 1 час": 1,
    "выкл. через 2 час": 2,
    "выкл. через 3 час": 3,
    "выкл. через 4 час": 4,
    "выкл. через 5 час": 5,
    "выкл. через 6 час": 6,
    "выкл. через 7 час": 7,
    "выкл. через 8 час": 8,
    "выкл. через 9 час": 9,
    "выкл. через 10 час": 10,
    "выкл. через 11 час": 11,
    "выкл. через 12 час": 12,
    "выкл. через 13 час": 13,
    "выкл. через 14 час": 14,
    "ручной режим": 15,
    "режим отладки": 16,
    "включен": 17
}



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



def get_actual_mode():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select value from device.complex_settings cs where param = 'load_work_mode'")
        s = cur.fetchone()
        if not s:
            return None, None
        mode_complex = s["value"]

        cur.execute("select value from device.complex_settings cs where param = 'device_load_working_mode'")
        s = cur.fetchone()
        if not s:
            return None, None

        return mode_complex, controller_modes_dict[s["value"]]



def redis_read(key_name, device_id="", additonal_params=""):
    key = key_name + str(device_id) + additonal_params
    payload = ''
    if r.exists(key):
        payload = r.get(key)
        return json.loads(payload)
    return ''



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
    r.set('command' + str(device_id), json.dumps(cmd))



def set_working_mode(mode):
    if mode >= 0x00 and mode <= 0x11:
        cmd = cmd_body('set_load_working_mode')
        cmd['value'] = mode
        r.set('command' + str(device_id), json.dumps(cmd))
    else:
        print('error mode')
    


def main():
    k = 0
    mode_complex, mode_controller = get_actual_mode()
    
    while True:
        k += 1
        time.sleep(1)
        if k > 2:
            mode_complex, mode_controller = get_actual_mode()
            print(mode_complex, mode_controller)
            k = 0

        if mode_complex == MODE_1:
            set_working_mode(mode_controller)
            r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 1)
        elif mode_complex == MODE_2:
            r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 0)
            set_working_mode(15)
            load_control(0)
        elif mode_complex == MODE_3:
            r.set(f'GPIO.{PIN_OUT_K3_LAMP}', 1)
            set_working_mode(15)
            load_control(1)
            
main()

