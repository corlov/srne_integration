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


def redis_read_v(key_name):
    r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
    if r.exists(key_name):        
        return r.get(key_name)
    return ''


print('mode', redis_read_v(RK_WIFI_STATUS))
print('error_text', redis_read_v(RK_WIFI_ERROR).decode('utf-8'))
print('error_details', redis_read_v(RK_WIFI_ERROR_DETAILS).decode('utf-8'))
quit()


r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
r.set(RK_WIFI_ON_REQ, 1)
time.sleep(15)
r.set(RK_WIFI_OFF_REQ, 1)

