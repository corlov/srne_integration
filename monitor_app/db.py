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



def clean_db():
    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()

        cursor.execute("delete from device.dynamic_information where created_at < NOW() - INTERVAL '14 days'")
        conn.commit()
        cursor.execute("delete from device.system_information where created_at < NOW() - INTERVAL '14 days'")
        conn.commit()
        cursor.execute("delete from device.command_history where created_at < NOW() - INTERVAL '14 days'")
        conn.commit()
        
        cursor.close()
        conn.close()

        u.logmsg('[OK]  clean')
    except Exception as e:
        u.logmsg(f"load_history_to_redis, Error occurred: {str(e)}", u.L_ERROR)        



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
            r.set(im.RK_HISTORY + str(glb.DEVICE_ID) + '_' + str(row[0]), json.dumps(row[1]))

        cursor.close()
        conn.close()

        u.logmsg('[OK]  load_history_to_redis')
    except Exception as e:
        u.logmsg(f"load_history_to_redis, Error occurred: {str(e)}", u.L_ERROR)        




def store_cmd(command):
    new_id = 0
    try:
        u.logmsg(command)
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
    
