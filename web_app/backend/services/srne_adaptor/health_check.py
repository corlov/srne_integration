import os
import glb_consts as glb
import time
import sys


try:
    # Get the modification time in seconds since the epoch
    modification_time = os.path.getmtime(os.path.join(glb.LOG_PATH, glb.MAIN_LOG_FILE))
    current_timestamp = time.time()    
    delta = current_timestamp - modification_time
    if delta > 120:
        print('timeout file change overflow')
        sys.exit(2)
        
    sys.exit(0)
except Exception as e:
    print("An error occurred:", e)
    sys.exit(1)
