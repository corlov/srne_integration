import os
import glb_consts as glb
import time
import sys
import redis
import utils as u

try:
    # Get the modification time in seconds since the epoch
    modification_time = os.path.getmtime(os.path.join(u.LOG_PATH, u.MAIN_LOG_FILE))
    current_timestamp = time.time()    
    delta = current_timestamp - modification_time
    if delta > glb.HEARTBEAT_UPD_TIMEOUT * 2:
        print('timeout file change overflow')
        sys.exit(2)
    print('chk 1 [ok]')
except Exception as e:
    print("An error occurred:", e)
    sys.exit(1)

try:
    import RepkaPi.GPIO as GPIO
    if not GPIO.getboardmodel():
        sys.exit(1)
    print('chk 2 [ok]')
except Exception as e:
    print("An error occurred:", e)
    sys.exit(2)

try:
    glb.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    glb.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    redis_time = float(r.get(glb.RK_HCHK).decode('utf-8'))
    if time.time() - redis_time > 30:
        sys.exit(3)

    print('chk 3 [ok]')
except Exception as e:
    print("An error occurred:", e)
    sys.exit(2)


sys.exit(0)
