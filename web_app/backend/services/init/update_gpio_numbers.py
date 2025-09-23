#!/usr/bin/python3

import psycopg2



PG_CONNECT_PARAMS = { 'dbname': 'solar_controller_telemetry', 'user': 'postgres', 'password': 'gen_postgress_password', 'host': '127.0.0.1', 'port': '5432' }

def update_data():
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(**PG_CONNECT_PARAMS)
        cursor = conn.cursor()

        # Список параметров для фильтрации
        params_to_filter = (
            'PIN_OUT_K2_TRAFFICLIGHT',
            'PIN_OUT_K3_LAMP',
            'PIN_OUT_K4_MODEM',
            'PIN_IN_CABINET_OPEN_DOOR_BUTTON',
            'PIN_IN_WIFI_BUTTON'
        )

        # Запрос для чтения данных из исходной таблицы
        source_query = """SELECT param, value FROM device.complex_settings WHERE param IN %s"""
        cursor.execute(source_query, (params_to_filter,))
        rows = cursor.fetchall()

        # Запрос для обновления данных в целевой таблице
        update_query = """UPDATE device.gpio_names SET pin = %s, uptime = now() WHERE code = %s"""

        for param, value in rows:
            # Преобразование значения value в integer
            pin_value = int(value)  # предполагаем, что value можно преобразовать в integer

            # Обновление данных в целевой таблице
            cursor.execute(update_query, (pin_value, param))

        # Сохранение изменений в базе данных
        conn.commit()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрытие соединений
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    update_data()