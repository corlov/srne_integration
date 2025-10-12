from psycopg2 import DatabaseError
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import glb_consts as glb


def logmsg(message, level="INFO", log_file='wifi.log'): 
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
    logmsg(f'{descr}, {name}, {type}, {severity}')
    
    conn = None
    try:
        conn = _get_conn()
        print('1')
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("insert into device.event_log (event_type, event_name, description, severity) values (%s, %s, %s, %s)", (type, name, descr, severity, ))
            print('2')
            conn.commit()
    except Exception as ex:
        logmsg(f"Ошибка при выполнении запроса к БД {ex}")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                logmsg("Ошибка при закрытии соединения с БД")


