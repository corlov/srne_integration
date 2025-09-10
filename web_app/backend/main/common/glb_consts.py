# FIXME: это с модулем GPIO общие настройки, их можно хранить в БД, например
PIN_OUT_K2_TRAFFICLIGHT = 22
PIN_OUT_K3_LAMP = 24
PIN_OUT_K4_MODEM = 26
PIN_IN_CABINET_OPEN_DOOR_BUTTON = 16
PIN_IN_WIFI_BUTTON = 18


SECRET_KEY = 'uw3cok92adxmzpf35_secret_key_value_12082025'


# TODO: затем это из переменных среды брать когда запускаем в контейнере
DB_HOST = 'localhost'
DB_NAME = 'solar_controller_telemetry'
DB_USER = 'postgres'
DB_PASSWORD = 'gen_postgress_password'
DB_PORT = '5432'



SSE_UPDATE_GPIO_TIMEOUT = 5
