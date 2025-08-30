import subprocess
import datetime
import time
import redis
import json
import uuid
import os
import psycopg2
from psycopg2 import sql


REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

RK_WIFI_STATUS = 'wifi_status'
RK_WIFI_ON_REQ = 'wifi_activate_on_request'
RK_WIFI_OFF_REQ = 'wifi_activate__off_request'
RK_WIFI_TS = 'wifi_activate_ts'
RK_WIFI_ERROR = 'wifi_error_text'
RK_WIFI_ERROR_DETAILS = 'wifi_error_text_details'

HOTSPOT_NAME = 'Hotspot'

r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)



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
    print(f'RUN CMD: {wifi_on}')
    res = run_command(wifi_on)
    time.sleep(1)
    return res



def send_activate_wifi_cmd(wifi_on):
    global r

    if wifi_on:
        error_details = ''
        error_details += run_command_sleep('nmcli radio wifi off')
        error_details += run_command_sleep('nmcli radio wifi on')
        error_details += run_command_sleep(f'nmcli con up {HOTSPOT_NAME}')
        res = run_command_sleep('ip -4 addr show wlan0')
        error_details += res

        #FIXME: подумать как передать в качестве параметра какую сеть должно запуститься
        if "192.168.4" not in res:
            print('ERR')
            r.set(RK_WIFI_ERROR, 'Не удалось активировать сеть')
            r.set(RK_WIFI_ERROR_DETAILS, error_details)
            r.set(RK_WIFI_STATUS, 'Откл.')
        else:
            print('OK')
            r.set(RK_WIFI_ERROR, '')
            r.set(RK_WIFI_ERROR_DETAILS, '')
            r.set(RK_WIFI_STATUS, 'Вкл.')
            
    else:
        error_details = ''
        error_details += run_command_sleep(f'nmcli con down {HOTSPOT_NAME}')
        error_details += run_command_sleep('nmcli radio wifi off')
        res = run_command_sleep('ip -4 addr show wlan0')
        error_details += res

        if "192.168.4" not in res:
            print('OK')
            r.set(RK_WIFI_ERROR, '')
            r.set(RK_WIFI_ERROR_DETAILS, '')
            r.set(RK_WIFI_STATUS, 'Откл.')
        else:
            print('ERR')
            r.set(RK_WIFI_ERROR, 'Не удалось деактивировать сеть')
            r.set(RK_WIFI_ERROR_DETAILS, error_details)
            r.set(RK_WIFI_STATUS, 'Вкл.')



def main():
    global r

    ts_activate_ts = 0

    if r.exists(RK_WIFI_TS):
        ts_activate_ts = int(r.get(RK_WIFI_TS))

        if int(time.time()) - int(ts_activate_ts) > 60*60:
            send_activate_wifi_cmd(False)
            ts_activate_ts = 0

    try:
        while True:
            print('tick', ts_activate_ts, int(time.time()) - ts_activate_ts)            
            time.sleep(1)

            if not is_connected(r):
                r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

            # есть команда включения Wifi?
            if r.exists(RK_WIFI_ON_REQ):
                req = int(r.get(RK_WIFI_ON_REQ))
                if req:
                    print('on Req, ', req)
                    ts_activate_ts = int(time.time())
                    r.set(RK_WIFI_TS, ts_activate_ts)
                    r.set(RK_WIFI_ON_REQ, 0)
                    send_activate_wifi_cmd(True)
            else:
                r.set(RK_WIFI_ON_REQ, 0)

            if ts_activate_ts > 0 and int(time.time()) - ts_activate_ts > 15:#60*60:
                send_activate_wifi_cmd(False)
                ts_activate_ts = 0


            # есть команда отключения Wifi?
            if r.exists(RK_WIFI_OFF_REQ):
                req = int(r.get(RK_WIFI_OFF_REQ))
                if req:
                    print('off Req, ', req)
                    r.set(RK_WIFI_OFF_REQ, 0)
                    send_activate_wifi_cmd(False)
                    ts_activate_ts = 0
            else:
                r.set(RK_WIFI_OFF_REQ, 0)
    finally:
        r.close()
    


if __name__ == '__main__':
    main()

