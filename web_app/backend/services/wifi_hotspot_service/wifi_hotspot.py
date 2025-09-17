#!/usr/bin/python3

import subprocess
import datetime
import time
import redis
import json
import uuid
import os

import db
import glb_consts as glb




def is_connected(redis_client):
    try:
        return redis_client.ping()
    except (redis.ConnectionError, redis.TimeoutError):
        return False


def run_command(command: str) -> str:
    """
    Run a system command and return the output as string.
    
    Args:
        command: Complete command string (e.g., "ls -l")
    
    Returns:
        Command output as string, or error message if failed
    """
    try:
        # Split the command string into list for subprocess
        cmd_list = command.split()
        print(cmd_list)
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
            
    except Exception as e:
        return f"Exception occurred: {str(e)}"



def run_command_sleep(wifi_on):
    res = run_command(wifi_on)
    time.sleep(1)
    return res



def send_activate_wifi_cmd(wifi_on):
    global r

    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set(glb.RK_WIFI_STATUS, 'Ожидание...')
    if wifi_on:
        error_details = ''
        error_details += run_command_sleep('nmcli radio wifi off')
        error_details += run_command_sleep('nmcli radio wifi on')
        error_details += run_command_sleep(f'nmcli con up {glb.HOTSPOT_NAME}')
        time.sleep(3)
        res = run_command_sleep('ip -4 addr show wlan0')
        error_details += res

        if glb.WIFI_NETWORK_PREFIX not in res:
            db.logmsg('ERR', 'res: ' + res, error_details)
            r.set(glb.RK_WIFI_ERROR, 'Не удалось активировать сеть')
            r.set(glb.RK_WIFI_ERROR_DETAILS, error_details)
            r.set(glb.RK_WIFI_STATUS, 'Откл.')
        else:
            db.logmsg('OK on')
            r.set(glb.RK_WIFI_ERROR, '')
            r.set(glb.RK_WIFI_ERROR_DETAILS, '')
            r.set(glb.RK_WIFI_STATUS, 'Вкл.')
            
    else:
        error_details = ''
        error_details += run_command_sleep(f'nmcli con down {glb.HOTSPOT_NAME}')
        error_details += run_command_sleep('nmcli radio wifi off')
        res = run_command_sleep('ip -4 addr show wlan0')
        error_details += res

        if glb.WIFI_NETWORK_PREFIX not in res:
            db.logmsg('OK off')
            r.set(glb.RK_WIFI_ERROR, '')
            r.set(glb.RK_WIFI_ERROR_DETAILS, '')
            r.set(glb.RK_WIFI_STATUS, 'Откл.')
        else:
            db.logmsg('ERR', 'res: ' + res, error_details)
            r.set(glb.RK_WIFI_ERROR, 'Не удалось деактивировать сеть')
            r.set(glb.RK_WIFI_ERROR_DETAILS, error_details)
            r.set(glb.RK_WIFI_STATUS, 'Вкл.')



def init():
    global PIN_OUT_K2_TRAFFICLIGHT

    glb.WIFI_NETWORK_PREFIX = os.getenv('WIFI_NETWORK_PREFIX', '192.168.4')
    glb.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    glb.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    glb.PG_CONNECT_PARAMS = { 
        'dbname': os.getenv('DB_NAME', 'solar_controller_telemetry'), 
        'user': os.getenv('DB_USER', 'postgres'), 
        'password': os.getenv('DB_PASSWORD', 'gen_postgress_password'), 
        'host': os.getenv('DB_HOST', 'localhost'), 
        'port': int(os.getenv('DB_PORT', 5432)), 
    }



def main():
    global r

    db.logmsg('started')
    init()

    db.event_log_add('запуск демона', 'wifi', 'EVENT', 'INFO')
    ts_activate_ts = 0

    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    if r.exists(glb.RK_WIFI_TS):
        ts_activate_ts = int(r.get(glb.RK_WIFI_TS))

        if int(time.time()) - int(ts_activate_ts) > 60*60:
            send_activate_wifi_cmd(False)
            ts_activate_ts = 0

    db.logmsg('init Redis [OK]')
    try:
        while True:
            cur_state = r.get(glb.RK_WIFI_STATUS).decode('utf-8') + '], on: ' + r.get(glb.RK_WIFI_ON_REQ).decode('utf-8') + ', off: '+ r.get(glb.RK_WIFI_OFF_REQ).decode('utf-8') + ', ts: '+r.get(glb.RK_WIFI_TS).decode('utf-8')
            print('tick [', cur_state)
            
            time.sleep(glb.DEBOUNCE_TIMEOUT)

            if not is_connected(r):
                r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

            # есть команда включения Wifi? 
            if r.exists(glb.RK_WIFI_ON_REQ):
                req = int(r.get(glb.RK_WIFI_ON_REQ))
                if req:
                    print('new command: on Req, ', req)
                    ts_activate_ts = int(time.time())
                    r.set(glb.RK_WIFI_TS, ts_activate_ts)
                    r.set(glb.RK_WIFI_ON_REQ, 0)
                    send_activate_wifi_cmd(True)
                    db.event_log_add('включение', 'wifi', 'EVENT', 'INFO')
            else:
                r.set(glb.RK_WIFI_ON_REQ, 0)

            if ts_activate_ts > 0 and int(time.time()) - ts_activate_ts > glb.HOLD_WIFI_ACTIVE_TIMEOUT_SECONDS:
                send_activate_wifi_cmd(False)
                ts_activate_ts = 0

            # есть команда отключения Wifi?
            if r.exists(glb.RK_WIFI_OFF_REQ):
                req = int(r.get(glb.RK_WIFI_OFF_REQ))
                if req:
                    print('new command: off Req, ', req)
                    r.set(glb.RK_WIFI_OFF_REQ, 0)
                    send_activate_wifi_cmd(False)
                    ts_activate_ts = 0
                    db.event_log_add('отключение', 'wifi', 'EVENT', 'INFO')
            else:
                r.set(glb.RK_WIFI_OFF_REQ, 0)
    finally:
        r.close()
    


if __name__ == '__main__':
    main()

