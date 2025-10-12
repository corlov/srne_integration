
import logging
import uuid

LOG_PATH = 'logs'
MAIN_LOG_FILE = 'gpio.log'

logging.basicConfig(level=logging.DEBUG, filename=MAIN_LOG_FILE, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



L_DEBUG = 0
L_INFO = 2
L_WARNING = 3
L_ERROR = 4
L_CRITICAL = 5


def logmsg(msg, level=L_INFO, arg=None):
    print(msg)

    if level == L_DEBUG:
        logging.debug(msg)
    else:
        logging.info(msg)