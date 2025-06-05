import traceback
import time
import json
from datetime import datetime
import redis
import psycopg2
import logging
import glb_consts as glb
import utils as u
import data_prepare as dp
import inmemory as im


def load_history_to_redis():
    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()

        cursor.execute("""
           select 
                TO_CHAR(actual_date, 'YYYY-MM-DD') as date,
                payload 
            from device.history h order by created_at desc limit 1024
        """)

        rows = cursor.fetchall()

        r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
        for row in rows:
            #print('history' + str(glb.DEVICE_ID) + '_' + str(row[0]))
            r.set(im.RK_HISTORY + str(glb.DEVICE_ID) + '_' + str(row[0]), json.dumps(row[1]))

    except Exception as e:
        print(f"load_history_to_redis, Error occurred: {type(e).__name__}: {e}")
        print("Line number:", traceback.extract_tb(e.__traceback__)[-1].lineno)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    u.logmsg('[OK]  load_history_to_redis')




def store_cmd(command):
    new_id = 0
    try:
        print(command)
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO device.command_history (device_id, payload)
            VALUES (%s, %s) RETURNING id;
        """
        cursor.execute(insert_query, (glb.DEVICE_ID, json.dumps(command),))
        new_id = cursor.fetchone()[0]
        conn.commit()
    except Exception as e:
        u.logmsg(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return new_id





# 0 - создана
# 1 - выполнена успешно
# 2 - ошибка
def store_cmd_status(id, status, err_text):
    if status:
        status = 1
    else: 
        status = 2
    
    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()
        insert_query = """
            UPDATE device.command_history 
            set status = %s, err_text = %s 
            where id = %s
        """
        cursor.execute(insert_query, (status, err_text, id, ))
        conn.commit()
    except Exception as e:
        u.logmsg(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
