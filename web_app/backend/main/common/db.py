import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError
import psycopg2.extras

import common.glb_consts as glb
import common.log as l
import common.utils as u



def get_conn():
    connection_params = {
        'host': glb.DB_HOST,
        'database': glb.DB_NAME,
        'user': glb.DB_USER,
        'password': glb.DB_PASSWORD,
        'port': glb.DB_PORT
    }
    try:
        return psycopg2.connect(**connection_params)
    except OperationalError as ex:
        l.logmsg("Не удалось установить соединение с БД")
        raise



def load_users():
    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Если SQL динамический — использовать psycopg2.sql; здесь статичный — безопасен
            cur.execute(
                """
                SELECT
                    cu.name AS username,
                    cu.hashed_password,
                    cr.name AS role
                FROM device.complex_user cu
                JOIN device.complex_role cr ON cr.id = cu.role_id
                """
            )
            rows = cur.fetchall()
            return rows
    except DatabaseError as ex:
        l.logmsg("Ошибка при выполнении запроса к БД")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                l.logmsg("Ошибка при закрытии соединения с БД")



def event_log_add(descr, name, type, severity):
    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = sql.SQL("""
                INSERT INTO {schema}.{table} ({col_event_type}, {col_event_name}, {col_description}, {col_severity})
                VALUES (%s, %s, %s, %s)
            """).format(
                schema=sql.Identifier('device'),
                table=sql.Identifier('event_log'),
                col_event_type=sql.Identifier('event_type'),
                col_event_name=sql.Identifier('event_name'),
                col_description=sql.Identifier('description'),
                col_severity=sql.Identifier('severity'),
            )
            cur.execute(query, (type, name, descr, severity))
            conn.commit()
    except DatabaseError as ex:
        l.logmsg("Ошибка при выполнении запроса к БД")
    except Exception as ex:
        l.logmsg(f"Unexpected error in event_log_add: {ex}")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                l.logmsg("Ошибка при закрытии соединения с БД")



def get_log(start_d, end_d, limit, sql_code):
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            query = sql.SQL(sql_code)
            cur.execute(query, (start_d, end_d, limit))
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows:
                item = {}
                for i, column in enumerate(columns):
                    item[column] = row[i]
                result.append(item)
            cur.close()
            conn.close()
 
            return result
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



def get_params_log(start_d, end_d, limit):
    sql_code = """
        select
            to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at,
            payload->'panels'->>'volts' as panel_volts,
            payload->'battery'->>'volts' as battery_volts,
            payload->'battery'->>'stateOfCharge' as battery_stateOfCharge,
            payload->'load'->>'amps' as load_amps,
            payload->'load'->>'dailyPower' as load_dailyPower,    
            payload->'controller'->>'chargingMode' as controller_chargingMode,
            payload->'load'->>'state' as load_state,
            payload->'controller'->>'temperature' as controller_temperature
        from solar_controller_telemetry.device.dynamic_information di
        where
            created_at between %s and %s
        order by created_at desc 
        limit %s;
    """
    return get_log(start_d, end_d, limit, sql_code)



def get_controller_internal_log(start_d, end_d, limit):
    sql_code = """
        select
            to_char(actual_date, 'YYYY-MM-DD HH24:MI:SS') as actual_date,
            payload->'currentDayMinBatteryVoltage' as currentDayMinBatteryVoltage,
            payload->'maxBatteryVoltage' as maxBatteryVoltage,
            payload->'maxChargingCurrent' as maxChargingCurrent,
            payload->'maxDischargingCurrent' as maxDischargingCurrent,
            payload->'maxChargingPower' as maxChargingPower,
            payload->'maxDischargingPower' as maxDischargingPower,
            payload->'chargingAmpHrs' as chargingAmpHrs,
            payload->'dischargingAmpHrs' as dischargingAmpHrs,
            payload->'powerGeneration' as powerGeneration,
            payload->'powerConsumption' as powerConsumption
        from solar_controller_telemetry.device.history h
        where
            actual_date between %s and %s
        order by actual_date desc 
        limit %s;
    """
    return get_log(start_d, end_d, limit, sql_code)



def get_events_log(start_d, end_d, limit, severity, event_type):
    conditions = ''    
    if severity:
        conditions += " and (severity = '" + severity + "')"
    if event_type:
        conditions += " and (event_type = '" + event_type + "')"

    sql_code = """
        select 
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at,
                event_type,
                event_name ,
                description,
                device_id,
                severity
            from solar_controller_telemetry.device.event_log di
            where
                created_at between %s and %s""" + conditions + """
            order by created_at desc 
            limit %s;
    """
    return get_log(start_d, end_d, limit, sql_code)


