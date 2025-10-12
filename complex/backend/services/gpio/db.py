from psycopg2 import DatabaseError
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import utils as u
import glb_consts as glb



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
        u.logmsg("Ошибка при выполнении запроса к БД")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                u.logmsg("Ошибка при закрытии соединения с БД")



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
        l.logmsg("Ошибка при выполнении запроса к БД")
        return {}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                l.logmsg("Ошибка при закрытии соединения с БД")
                return {}



def get_pin_by_code(code):
    row = _get_one_row(f"select pin from device.gpio_names where code = '{code}'")
    return row['pin']
