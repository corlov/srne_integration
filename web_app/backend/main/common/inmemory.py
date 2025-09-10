import redis
import json
import os

REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

RK_TELEMETRY = 'telemetry'
RK_SYS_INFO = 'system_information'
RK_SETTINGS = 'eeprom_parameter_setting'
RK_COMMAND = 'command'
RK_HISTORY = 'history'
RK_COMMAND_RESPONSE = 'commands_responses'


RK_WIFI_STATUS = 'wifi_status'
RK_WIFI_ON_REQ = 'wifi_activate_on_request'
RK_WIFI_OFF_REQ = 'wifi_activate_off_request'
RK_WIFI_TS = 'wifi_activate_ts'
RK_WIFI_ERROR = 'wifi_error_text'
RK_WIFI_ERROR_DETAILS = 'wifi_error_text_details'


def redis_read_json(key_name, device_id="", additonal_params=""):
    try:
        r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
        key = key_name + str(device_id) + additonal_params
        payload = ''
        if r.exists(key):
            payload = r.get(key)
            return json.loads(payload)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ''
    return ''


def redis_read_v(key_name):
    try:
        r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
        if r.exists(key_name):
            return r.get(key_name)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ''
    return ''



def redis_set(key, value):
    try:
        r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
        r.set(key, value)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def redis_get(key):
    try:
        r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
        return r.get(key)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
