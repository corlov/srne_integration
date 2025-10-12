from psycopg2 import DatabaseError
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import glb_consts as glb


def logmsg(message, level="INFO", log_file='traf_ligth_mode.log'): 
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level.upper()}]: {message}"
    
    print(log_entry)
    
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')


def _get_conn():
    return psycopg2.connect(**glb.PG_CONNECT_PARAMS)



def event_log_add(descr, name, type, severity):
    conn = None
    try:
        conn = _get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("insert into device.event_log (event_type, event_name, description, severity) values (%s, %s, %s, %s)", (type, name, descr, severity, ))
            conn.commit()
    except Exception as ex:
        logmsg("Ошибка при выполнении запроса к БД")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                logmsg("Ошибка при закрытии соединения с БД")


def _get_one_row(sql_code):
    try:
        conn = _get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = sql.SQL(sql_code)
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            conn.close()
            return row
    except DatabaseError as ex:
        logmsg("Ошибка при выполнении запроса к БД")
        return {}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                logmsg("Ошибка при закрытии соединения с БД")
                return {}



def get_pin_by_code(code):
    row = _get_one_row(f"select pin from device.gpio_names where code = '{code}'")
    return row['pin']



def get_actual_mode():
    conn = None
    try:
        conn = _get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("select value from device.complex_settings cs where param = 'trafficlight_work_mode'")
            s = cur.fetchone()
            if not s:
                return None
            return s["value"]
    except Exception as ex:
        logmsg("Ошибка при выполнении запроса к БД")
        return None
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                logmsg("Ошибка при закрытии соединения с БД")
                return None

