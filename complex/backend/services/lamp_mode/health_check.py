import os
import time
import sys


LOG_PATH = 'logs'
MAIN_LOG_FILE = 'app.log'

try:
    # Get the modification time in seconds since the epoch
    modification_time = os.path.getmtime(os.path.join(LOG_PATH, MAIN_LOG_FILE))
    current_timestamp = time.time()    
    delta = current_timestamp - modification_time
    if delta > 2*60:
        print('timeout file change overflow')
        sys.exit(2)
    print('chk 1 [ok]')
except Exception as e:
    print("An error occurred:", e)
    sys.exit(1)

sys.exit(0)
