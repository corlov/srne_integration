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
        cursor.execute("DELETE FROM device.eeprom_parameter_setting WHERE created_at < NOW() - INTERVAL '14 days' AND created_at < (SELECT MAX(created_at) FROM device.eeprom_parameter_setting)")
        conn.commit()
        cursor.execute("DELETE FROM device.event_log WHERE created_at < NOW() - INTERVAL '365 days'")
        conn.commit()
        cursor.execute("delete from device.history where created_at < NOW() - INTERVAL '1024 days'")
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
    


def read_settings_from_db():
    cursor = None
    conn = None
    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()
        query = """
            select 
                (select value from device.complex_settings where param = 'commands_debounce_seconds') as cmd,
                (select value from device.complex_settings where param = 'solar_panel_state_debounce_seconds') as state
        """
        cursor.execute(query)

        row = cursor.fetchone()
        cmd_timeout, state_timeout = row[0], row[1]        
        cursor.close()
        conn.close()

        print('read_settings_from_db', cmd_timeout, state_timeout)
        return int(cmd_timeout), int(state_timeout)
    except Exception as e:
        u.logmsg(f"An error occurred: {e}", u.L_ERROR)
        return None, None