#!/usr/bin/python3

import os
import atexit
import time
import json
import redis
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial
from datetime import datetime, timedelta
import logging
import glb_consts as glb
import utils as u
import data_prepare as dp
import db
import SRNE as srne
import send_commands as sc
import inmemory as im


modbus = None
StateTimeout = glb.DELAY_BETWEEN_REQUESTS
CmdTimeout = glb.DELAY_BETWEEN_COMMANDS


def init():
    global CmdTimeout
    global StateTimeout

    StateTimeout = glb.DELAY_BETWEEN_REQUESTS
    CmdTimeout = glb.DELAY_BETWEEN_COMMANDS

    if not os.path.exists(glb.LOG_PATH):
        os.makedirs(glb.LOG_PATH)    

    log_file = os.path.join(glb.LOG_PATH, glb.MAIN_LOG_FILE)
    if os.path.exists(log_file):
        size_limit = 1024*1024*30  # 30Mb
        file_size = os.path.getsize(log_file)
        if file_size > size_limit:
            try:
                os.remove(log_file)
            except:
                print(f"cant remove the log file")
    
    logging.basicConfig(filename=log_file, force=True, level=logging.DEBUG, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    glb.DEVICE_ID = int(os.getenv('DEVICE_ID', 2))
    glb.DEVICE_SYS_ADDR = os.getenv('DEVICE_SYS_ADDR', '/dev/ttyS0')
    
    glb.REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
    glb.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    glb.PG_CONNECT_PARAMS = { 
        'dbname': os.getenv('DB_NAME', 'solar_controller_telemetry'), 
        'user': os.getenv('DB_USER', 'postgres'), 
        'password': os.getenv('DB_PASSWORD', 'gen_postgress_password'), 
        'host': os.getenv('DB_HOST', 'localhost'), 
        'port': int(os.getenv('DB_PORT', 5432)), 
    }
    glb.PUBLISH_BROKER_ENABLED = os.getenv('PUBLISH_BROKER_ENABLED', True)
    glb.MQTT_SERVER_ADDR = os.getenv('MQTT_SERVER_ADDR', "127.0.0.1")
    glb.MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
    glb.MQTT_USER = os.getenv('MQTT_USER', 'srne_user')
    glb.MQTT_PASS = os.getenv('MQTT_PASS', 'qwe123')

    CmdTimeout, StateTimeout = db.read_settings_from_db()
    print(CmdTimeout, StateTimeout)

    im.flush_keys()

    u.logmsg("[OK]  init")



# When program exits, close the modbus connection.
def exit_handler():
    global modbus
    u.logmsg("\nClosing Modbus Connection...")
    modbus.close()

atexit.register(exit_handler)



def read_data():
    global modbus
    dp.read_dynamic_payload(modbus)
    dp.read_system_information(modbus)
    dp.read_controller_settings(modbus)
    dp.read_history(modbus)
    dp.read_system_information(modbus)



def exec_command(cmd):
    u.logmsg(f"exec_command: {cmd['command']}")
    u.logmsg(cmd, u.L_DEBUG)
    
    if ('user' not in cmd) or (not cmd['user']):
        return False, "user field hasnt filled"
    if ('created_at' not in cmd) or (not cmd['created_at']):
        return False, "created_at field hasnt filled"
    if ('uuid' not in cmd) or (not cmd['uuid']):
        return False, "uuid field hasnt filled"
    if abs(datetime.now().timestamp() - float(cmd['created_at'])) > glb.DELAY_BETWEEN_COMMANDS*2:
        return False, "Command time is expired"

    match cmd['command']:
        case "control_load_on_off":
            on_off = int(cmd['value'])
            if 0 == on_off or 1 == on_off:
                return sc.send2device(srne.addr_loadOnOff, on_off)
            else:
                return False, "Unknown mode"
        
        case "clear_history":
            return sc.exec_special_command(srne.cmd_clear_history)
        
        case "reset_to_factory_default_settings":
            return sc.exec_special_command(srne.cmd_reset_settings)

        case "set_load_working_mode":
            mode = int(cmd['value'])
            if mode >= 0x00 and mode <= 0x11:
                return sc.send2device(srne.addr_loadWorkingMode, mode)
            else:
                return False, "Unknown mode"

        #TODO: только последний параметр успешно записывается в девайс
        case "set_parameters":
            parameters = cmd['parameters']
            return sc.set_parameters(parameters)

        case "set_charge_current":
            current_amp = float(cmd['value'])
            if current_amp >= 0.01 and current_amp < 30:
                current_amp = int(current_amp * 100)
                return sc.send2device(srne.addr_chargeCurrent, current_amp)
            else:
                return False, "Incorrect current value was passed"

        case _:
            return False, "Unrecognized command"



def run():
    import pymodbus
    u.logmsg(f"*** pymodbus version: {pymodbus.__version__} ***")

    global CmdTimeout
    global StateTimeout
    global modbus

    print(CmdTimeout, StateTimeout)

    db.load_history_to_redis()
    db.clean_db()

    previous_time_cmd = datetime.now() - timedelta(seconds=CmdTimeout)
    previous_time_save_state = datetime.now() - timedelta(seconds=StateTimeout)
    cleanup_counter = 0
    t = 0
    first_loop = True
    while True:
        time.sleep(1)
        current_time = datetime.now()
        
        if (current_time - previous_time_cmd) > timedelta(seconds=CmdTimeout):
            previous_time_cmd = current_time
            command_str = sc.get_external_command()
            if command_str is None:
                u.logmsg(f"empty command")
                if modbus:
                    if modbus.connect():
                        modbus.close()
                continue
            elif command_str:
                command = json.loads(command_str)
                u.logmsg(f"command: {command}")
                id = db.store_cmd(command)
                if id:
                    status, err_text = exec_command(command)
                    u.logmsg(f"status: {status}, error: {err_text}")
                    db.store_cmd_status(id, status, err_text)
                    im.store_command_response(id, command['uuid'], status, err_text)
        
        
        if (current_time - previous_time_save_state) > timedelta(seconds=StateTimeout):
            u.logmsg("save state")
            previous_time_save_state = current_time

            db.clean_db()
            CmdTimeout, StateTimeout = db.read_settings_from_db()

            try:
                modbus = ModbusClient(port=glb.DEVICE_SYS_ADDR, baudrate=9600, stopbits=1, bytesize=8, parity='N', timeout=5)
                if modbus.connect():
                    read_data()
                    u.logmsg(f"== tick {current_time}=============================")
                    modbus.close()
                else:
                    u.logmsg(f"Failed to connect to Modbus server INIT '{glb.DEVICE_SYS_ADDR}'")
            except Exception as e:
                u.logmsg(e)



if __name__ == '__main__':
    init()
    run()

