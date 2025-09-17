REDIS_ADDR = 'localhost'
REDIS_PORT = 6379
RK_TELEMETRY = 'telemetry'

DEVICE_ID = 2

MODE_1 = "режим 1 (1Гц, 500мс)"
MODE_2 = "режим 2 (1Гц, 100мс)"
MODE_3 = "режим 3 (алгоритм)"
MODE_4 = "режим 4 (откл.)"


HI_VOLTAGE = 11.2
LOW_VOLTAGE = 10.2

PG_CONNECT_PARAMS = { 'dbname': 'solar_controller_telemetry', 'user': 'postgres', 'password': 'gen_postgress_password', 'host': '127.0.0.1', 'port': '5432' }