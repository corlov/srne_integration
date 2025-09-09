import json
import redis
import time
import glb_consts as glb
import utils as u


RK_TELEMETRY = 'telemetry'
RK_SYS_INFO = 'system_information'
RK_SETTINGS = 'eeprom_parameter_setting'
RK_COMMAND = 'command'
RK_HISTORY = 'history'
RK_COMMAND_RESPONSE = 'commands_responses'



def store_command_response(id, uuid, status, err_text):
    resp = {}
    resp['dbId'] = id
    resp['uuid'] = uuid
    resp['ts'] = time.time()
    resp['ok'] = status
    resp['errorText'] = err_text

    try:
        r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
        r.rpush(RK_COMMAND_RESPONSE, json.dumps(resp))

        # Retrieve the existing list from Redis
        commands_list = r.lrange(RK_COMMAND_RESPONSE, 0, -1)
        commands_list = [item.decode('utf-8') for item in commands_list]

        target_response = {}

        fresh_commands = []
        for cmd in commands_list:
            cmd = json.loads(cmd)
            ts = float(cmd['ts'])
            if time.time() - ts < 5*60:
                fresh_commands.append(cmd)

        # Обновляем список ответов, удалив протухшие ответы по времени
        r.delete(RK_COMMAND_RESPONSE)
        for cmd in fresh_commands:
            r.rpush(RK_COMMAND_RESPONSE, json.dumps(cmd))
    except Exception as e:
        u.logmsg(f"store_command_response, An error occurred: {e}", u.L_ERROR)
        return

    u.logmsg('[OK] store_command_response')



def flush_keys():
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set(RK_SETTINGS + str(glb.DEVICE_ID), '')
    r.set(RK_SYS_INFO + str(glb.DEVICE_ID), '')
    

