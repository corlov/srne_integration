REDIS_ADDR = 'localhost'
REDIS_PORT = 6379

LOG_PATH = 'logs'
MAIN_LOG_FILE = 'solar_monitor.log'

PG_CONNECT_PARAMS = { 'dbname': 'solar_controller_telemetry', 'user': 'postgres', 'password': 'gen_postgress_password', 'host': '127.0.0.1', 'port': '5432' }

# Number of seconds to wait in between requests to the charge controller.
DELAY_BETWEEN_REQUESTS = 600
DELAY_BETWEEN_COMMANDS = 2

CLEANUP_LIMIT = DELAY_BETWEEN_COMMANDS * 100

DEVICE_ID = 2
DEVICE_SYS_ADDR = '/dev/ttyS0'
DEVICE_SERIAL_NUMBER = ''


# Array of charging mode strings.
# These are the states the charge controller can be in when charging the battery.
chargeModes = [
    "OFF",      #0
    "NORMAL",   #1
    "MPPT",     #2
    "EQUALIZE", #3
    "BOOST",    #4
    "FLOAT",    #5
    "CUR_LIM"   #6 (Current limiting)
]

faultCodes = [
    "Charge MOS short circuit",      #0
    "Anti-reverse MOS short",        #1
    "PV panel reversely connected",  #2
    "PV working point over voltage", #3
    "PV counter current",            #4
    "PV input side over-voltage",    #5
    "PV input side short circuit",   #6
    "PV input overpower",            #7
    "Ambient temp too high",         #8
    "Controller temp too high",      #9
    "Load over-power/current",       #10
    "Load short circuit",            #11
    "Battery undervoltage warning",  #12
    "Battery overvoltage",           #13
    "Battery over-discharge"         #14
]



UNIT_VOLT = 'V'
UNIT_AMPERE = 'A'
UNIT_AH = 'AH'
UNIT_WATT = 'WATT'
UNIT_STRING = 'string'
UNIT_SECOND = 'second'
UNIT_MINUTE = 'minute'
UNIT_DAY = 'day'
UNIT_MV = 'mV'


DEVICE_TYPE_CONTROLLER = 'controller'
DEVICE_TYPE_INVERTER = 'inverter'



workingModes = [
    'Sole light control, light control over on/ off of load',
    'Load is turned on by light control, and goes off after a time delay of 1 hour',
    'Load is turned on by light control, and goes off after a time delay of 2 hours',
    'Load is turned on by light control, and goes off after a time delay of 3 hours',
    'Load is turned on by light control, and goes off after a time delay of 4 hours',
    'Load is turned on by light control, and goes off after a time delay of 5 hours',
    'Load is turned on by light control, and goes off after a time delay of 6 hours',
    'Load is turned on by light control, and goes off after a time delay of 7 hours',
    'Load is turned on by light control, and goes off after a time delay of 8 hours',
    'Load is turned on by light control, and goes off after a time delay of 9 hours',
    'Load is turned on by light control, and goes off after a time delay of 10 hours',
    'Load is turned on by light control, and goes off after a time delay of 11 hours',
    'Load is turned on by light control, and goes off after a time delay of 12 hours',
    'Load is turned on by light control, and goes off after a time delay of 13 hours',
    'Load is turned on by light control, and goes off after a time delay of 14 hours',
    'Manual mode',
    'Debugging mode',
    'Normal on mode',
]


batteryTypes = [
    "custom",      #0
    "open",   #1
    "sealed",     #2
    "gel", #3
    "lithium",    #4
]

# отправлять данные в брокер или нет
PUBLISH_BROKER_ENABLED = False
