import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError
import psycopg2.extras
from flask import jsonify
from flask import abort
import common.glb_consts as glb
import common.log as l
import common.utils as u



def _get_conn():
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
        l.logmsg(f"Не удалось установить соединение с БД {glb.DB_HOST}:{glb.DB_PORT} {glb.DB_NAME}")
        raise



def load_users():
    conn = None
    try:
        conn = _get_conn()
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

# type:     ERROR EVENT
# severity: DEBUG INFO WARNING ERROR
def event_log_add(descr, name, type, severity):
    l.logmsg(f'{descr}, {name}, {type}, {severity}')

    conn = None
    try:
        conn = _get_conn()
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



def _get_log(start_d, end_d, limit, sql_code):
    try:
        conn = _get_conn()
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
    return _get_log(start_d, end_d, limit, sql_code)



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
    return _get_log(start_d, end_d, limit, sql_code)



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
    return _get_log(start_d, end_d, limit, sql_code)



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



def get_time_source():
    sql_code = """
        SELECT 
                MAX(CASE WHEN param = 'time_source' THEN value END) as src,
                MAX(CASE WHEN param = 'time_source_addr' THEN value END) as addr
            FROM device.complex_settings
            WHERE param IN ('time_source', 'time_source_addr')
    """
    row = _get_one_row(sql_code)
    print(row)
    if not row:
        return None, None
    else:
        return row["src"], row["addr"]



def _get_dataset(sql_code):
    try:
        conn = _get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = sql.SQL(sql_code)
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
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



def get_complex_settings():
    ds = _get_dataset("""
        select 
            id, 
            descr as name, 
            value, 
            type, 
            options, 
            param 
        from device.complex_settings cs 
        order by ui_field_order""")

    return jsonify(ds)




def clear_log(log_table_name):
    try:
        conn = _get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = sql.SQL(f"truncate device.{log_table_name}")
            cur.execute(query)
            conn.commit()
            return rows
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



def update_complex_setting(setting_id, new_value):
    with _get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                id, 
                descr as name, 
                type, 
                options 
            FROM device.complex_settings WHERE id = %s""", (setting_id,))
        s = cur.fetchone()
        if not s:
            return abort(404)
        t = s["type"]
        opts = s.get("options")

        # Simple validation/conversion
        if t == "boolean":
            if not isinstance(new_value, bool):
                # allow strings 'true'/'false'
                if isinstance(new_value, str) and new_value.lower() in ("true","false"):
                    new_value = new_value.lower() == "true"
                else:
                    return abort(400, "Invalid boolean")
            store_value = "true" if new_value else "false"
        elif t == "select":
            if opts is None:
                return abort(500, "No options defined")
            if new_value not in opts:
                return abort(400, "Invalid option")
            store_value = str(new_value)
        else:  # string or default
            store_value = str(new_value)

        cur.execute("UPDATE device.complex_settings SET value = %s WHERE id = %s", (store_value, setting_id))
        conn.commit()
        return jsonify({"ok": True})



def get_complex_param_val_settings():
    ds = _get_dataset("""
            SELECT 
                param, 
                value 
            FROM solar_controller_telemetry.device.complex_settings 
            order by ui_field_order""")

    result_dict = {}
    for row in ds:
        result_dict[row['param']] = row['value']
    
    return result_dict



def get_timeseries_fro_charts():
    ds = _get_dataset("""
        select *
        from
        (
            SELECT 
                    (di.created_at AT TIME ZONE 'UTC')::date AS ts,
                    avg((di.payload -> 'controller' ->> 'temperature')::int) AS controller_temperature,
                    avg((di.payload -> 'battery' ->> 'temperature')::int) AS battery_temperature,
                    avg((di.payload -> 'battery' ->> 'volts')::float) AS battery_volts
            FROM device.dynamic_information di
            WHERE 
                di.payload ? 'controller' 
                AND (di.payload -> 'controller') ? 'temperature'
                AND di.payload ? 'battery' 
                AND (di.payload -> 'battery') ? 'temperature'
                AND (di.payload -> 'battery') ? 'volts'
            group by ts	
            ORDER BY ts
        ) as t1
        join (
            select
                h.actual_date::date as ts,
                avg((h.payload->'maxBatteryVoltage')::int) as maxv,
                avg((h.payload->'currentDayMinBatteryVoltage')::int) as minv
            from device.history h
            group by h.actual_date::date 	
            ORDER BY h.actual_date::date
        ) as t2 on t1.ts = t2.ts
    """)
    return ds


def get_pin_by_code(code):
    row = _get_one_row(f"select pin from device.gpio_names where code = '{code}'")
    return row['pin']



