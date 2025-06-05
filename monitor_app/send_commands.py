import time
import json
import redis
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial
from datetime import datetime
import psycopg2
import logging
import glb_consts as glb
import utils as u
import data_prepare as dp
import db
import SRNE as srne
import inmemory as im



def send2device(addr, value):
    global modbus

    u.logmsg(f'send2device: {addr} {value}', u.L_DEBUG)

    try:
        modbus = ModbusClient(port=glb.DEVICE_SYS_ADDR, baudrate=9600, stopbits=1, bytesize=8, parity='N', timeout=5)
        if modbus.connect():
            result = modbus.write_register(addr, value, slave=glb.DEVICE_ID)
            modbus.close()
        else:
            return False, "Failed to connect to Modbus server INIT"
    except Exception as e:
        return False, "Error modbus: " + str(e)

    if result.isError():
        return False, "Error writing to register: " + str(result)
    
    return True, ''



def get_external_command():
    client = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    command = client.get(im.RK_COMMAND + str(glb.DEVICE_ID))
    client.set(im.RK_COMMAND + str(glb.DEVICE_ID), '')
    client.close()
    return command



def set_parameters(parameters):
    if len(parameters) != 16:
        return False, "incorect params count"

    for i in range(0, 10):
        parameters[i] = int(parameters[i] * 10)
    
    for i in range(10, 16):
        parameters[i] = int(parameters[i])
    
    # TODO: так только последний параметр - температурный коэффициент дает поменять и все.... 
    # почему-то если руками задавать параметры через виндовую программу настройки, то дает вроде бы
    for i in range(0, 16):
        send2device(0xE005 + i, parameters[i])
        time.sleep(1)

    return True, ''

    # второй вариант как в документации описано отправляю 10 команду и сразу все записать пробую, тоже не записываются
    header = bytes([
        glb.DEVICE_ID, 
        0x10, 
        0xE0, 0x05, 
        0x00, 0x10, 0x20
    ])

    body = []
    for i in range(0, 16):
        low_byte = int(parameters[i]) & 0xFF
        high_byte = (int(parameters[i]) >> 8) & 0xFF
        body.append(high_byte)
        body.append(low_byte)

    print(f"body: {body}")
    
    cmd = header + bytes(body)

    hex_output = ' '.join(f'{byte:02x}' for byte in cmd)
    print(f"Cmd: {hex_output}")

    try:
        with serial.Serial(glb.DEVICE_SYS_ADDR, 9600, timeout=5) as ser:
            
            crc_bytes = u.modbus_crc(cmd).to_bytes(2, byteorder='little')
            raw_data = cmd + crc_bytes

            hex_output = ' '.join(f'{byte:02x}' for byte in raw_data)
            print(f"raw_data: {hex_output}")

            bytes_written = ser.write(raw_data)
            ser.flush()
            data = ser.read(size=8)
            u.logmsg(f"Received: {data}, {data.hex()}")
            if not data:
                return False, "No response from device"
            
            print(data[0], data[1], data[2], data[3], data[4], data[5])

            # TODO: почему не устаеналиваются настройки? успешный код приходит...
            if not(data[0] == glb.DEVICE_ID and data[1] == 0x10 and data[2] == 0xE0 and data[3] == 0x05 and data[4] == 0x00 and data[5] == 0x10):
                r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
                r.set(im.RK_SETTINGS + str(glb.DEVICE_ID), '')
                return False, data.hex()
    except Exception as e:
        u.logmsg(e)
        return False, e

    return True, ''



def exec_special_command(special_cmd_code):
    cmd = bytes([glb.DEVICE_ID, special_cmd_code, 0x00, 0x00, 0x00, 0x01])

    try:
        with serial.Serial(glb.DEVICE_SYS_ADDR, 9600, timeout=5) as ser:
            
            crc_bytes = u.modbus_crc(cmd).to_bytes(2, byteorder='little')
            raw_data = cmd + crc_bytes

            bytes_written = ser.write(raw_data)
            ser.flush()
            data = ser.read(size=8)
            u.logmsg(f"Received: {data}, {data.hex()}")
            if not data:
                return False, "No response from device"
            
            if data != raw_data:
                return False, "Response from device isn't OK"
    except Exception as e:
        u.logmsg(e)
        return False, e

    return True, ''

