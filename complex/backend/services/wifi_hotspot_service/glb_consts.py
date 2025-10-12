REDIS_ADDR = 'localhost'
REDIS_PORT = 6379


RK_WIFI_STATUS = 'wifi_status'
RK_WIFI_ON_REQ = 'wifi_activate_on_request'
RK_WIFI_OFF_REQ = 'wifi_activate_off_request'
RK_WIFI_TS = 'wifi_activate_ts'
RK_WIFI_ERROR = 'wifi_error_text'
RK_WIFI_ERROR_DETAILS = 'wifi_error_text_details'

HOTSPOT_NAME = 'Hotspot'

WIFI_NETWORK_PREFIX = '192.168.4'

PG_CONNECT_PARAMS = { 'dbname': 'solar_controller_telemetry', 'user': 'postgres', 'password': 'gen_postgress_password', 'host': '127.0.0.1', 'port': '5432' }

# сколько держать активированой точку доступа после нажатия кнопки
HOLD_WIFI_ACTIVE_TIMEOUT_SECONDS = 60*60


DEBOUNCE_TIMEOUT = 1

