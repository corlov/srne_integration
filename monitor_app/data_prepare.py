import traceback
import time
import json
import redis
from pymodbus.client import ModbusSerialClient as ModbusClient
from datetime import datetime
import psycopg2
import logging
import glb_consts as glb
import utils as u
import db
import inmemory as im
import SRNE as sr
import broker as br


# Convert the register data to a JSON string. (For JSON print option)
def dynamic_info_jsonfy(response, error):
    json_string = ""
    nested_dict = {}

    if(error):
        nested_dict = {
            "modbusError": error,
        }
    else:
        # Offset to apply when determining the charging mode.
        # This only applies when the load is turned on since they share a register.
        loadOffset = 32768 if response.registers[32] > 6 else 0

        # Determine if there are any faults / what they mean.
        faults = []
        faultID = response.registers[34]
        if(faultID != 0):
            count = 0
            while(faultID != 0):
                if(faultID >= pow(2, 15-count)):
                    faults.append(glb.faultCodes[count-1])
                    faultID -= pow(2, 15-count)
                count += 1

        nested_dict = {
            "modbusError": error,
            "controller": {
                "chargingMode": glb.chargeModes[response.registers[32]-loadOffset],
                "temperature": u.getRealTemp(int(hex(response.registers[3])[2:-2], 16)),
                "days": response.registers[21],
                "overDischarges": response.registers[22],
                "fullCharges": response.registers[23]
            },
            "charging": {
                "amps": round(float(response.registers[2]*0.01), 2),
                "maxAmps": round(float(response.registers[13]*0.01), 2),
                "watts": response.registers[9],
                "maxWatts": response.registers[15],
                "dailyAmpHours": response.registers[17],
                "totalAmpHours": round(float((response.registers[24]*65536 + response.registers[25])*0.001), 3),
                "dailyPower": round(float(response.registers[19]*0.001), 3),
                "totalPower": round(float((response.registers[28]*65536 + response.registers[29])*0.001), 3)
            },
            "battery": {
                "stateOfCharge": response.registers[0],
                "volts": round(float(response.registers[1]*0.1), 1),
                "minVolts": round(float(response.registers[11]*0.1), 1),
                "maxVolts": round(float(response.registers[12]*0.1), 1),
                "temperature": u.getRealTemp(int(hex(response.registers[3])[-2:], 16))
            },
            "panels": {
                "volts": round(float(response.registers[7]*0.1), 1),
                "amps": round(float(response.registers[8]*0.01), 2)
            },
            "load": {
                "state": True if response.registers[10] else False,
                "volts": round(float(response.registers[4]*0.1), 1),
                "amps": round(float(response.registers[5]*0.01), 2),
                "watts": response.registers[6],
                "maxAmps": response.registers[14]*0.01,
                "maxWatts": response.registers[16],
                "dailyAmpHours": response.registers[18],
                "totalAmpHours": round(float((response.registers[26]*65536 + response.registers[27])*0.001), 3),
                "dailyPower": round(float(response.registers[20]*0.001), 3),
                "totalPower": str(round(float((response.registers[30]*65536 + response.registers[31])*0.001), 3))
            },
            "faults": faults
        }
    json_string = json.dumps(nested_dict, indent=4)
    return json_string



def read_dynamic_payload(modbus):
    response = modbus.read_holding_registers(address=sr.addr_dynamic_info_registers_start_addr, count=35, slave=glb.DEVICE_ID)
    payload = dynamic_info_jsonfy(response, False)

    # последнюю информацию писать в кеш
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    r.set(im.RK_TELEMETRY + str(glb.DEVICE_ID), payload)

    if glb.PUBLISH_BROKER_ENABLED:
        br.publish(br.TOPIC_TELEMETRY, payload)

    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO device.dynamic_information (payload)
            VALUES (%s);
        """
        cursor.execute(insert_query, (payload,))
        conn.commit()
        u.logmsg('[OK]  read_dynamic_payload')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




def read_history(modbus):
    try:
        conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
        cursor = conn.cursor()

        # формируем таблицу из 1023 строк, если есть информация за дату то дифф значений будет 0, 
        # иначе полезем в устройство и считаем исторические данные и добавим в БД
        cursor.execute("""
            select 
                t.number,
                t.number - coalesce(EXTRACT(DAY FROM NOW() - actual_date), 0) as d
            from
                (SELECT generate_series(1, 1024) AS number) as t
            left join device.history as h 
                on t.number = EXTRACT(DAY FROM NOW() - actual_date) 
                    and h.device_id = %s 
                    and actual_date >= now() - INTERVAL '1024 days';
        """, (glb.DEVICE_ID,))

        rows = cursor.fetchall()
        updated = False
        for row in rows:
            # время постоячнно увеличивается и если этой проверки нет то постоянно будет добавляться информация по 1023 дню как будто бы ее нет
            if row[0] >= 1024:
                break
            if row[1]:
                updated = True
                day = row[0]
                #history_data_length = 10
                addr = sr.add_history_start_addr + day # * history_data_length
                response = modbus.read_holding_registers(address=addr, count=10, slave=glb.DEVICE_ID)
                
                payload = {
                    'currentDayMinBatteryVoltage': response.registers[0], 'unit': glb.UNIT_VOLT,
                    'maxBatteryVoltage': response.registers[1], 'unit': glb.UNIT_VOLT,
                    'maxChargingCurrent': response.registers[2], 'unit': glb.UNIT_AMPERE,
                    'maxDischargingCurrent': response.registers[3], 'unit': glb.UNIT_AMPERE,
                    'maxChargingPower': response.registers[4], 'unit': glb.UNIT_AH,
                    'maxDischargingPower': response.registers[5], 'unit': glb.UNIT_AH,
                    'chargingAmpHrs': response.registers[6], 'unit': glb.UNIT_AH,
                    'dischargingAmpHrs': response.registers[7], 'unit': glb.UNIT_AH,
                    'powerGeneration': response.registers[8], 'unit': glb.UNIT_AH,
                    'powerConsumption': response.registers[9], 'unit': glb.UNIT_AH,
                }
                insert_query = """
                    INSERT INTO device.history(day, payload, device_id, actual_date) 
                    VALUES (%s,%s,%s, now() - INTERVAL '%s days');
                """
                cursor.execute(insert_query, (day, json.dumps(payload), glb.DEVICE_ID, day))
                conn.commit()
                u.logmsg(f'history added, day {day}', u.L_DEBUG)

        if updated:
            db.load_history_to_redis()
    except Exception as e:
        #print(f"An error occurred: {e}")
        print(f"Error occurred: {type(e).__name__}: {e}")
        print("Line number:", traceback.extract_tb(e.__traceback__)[-1].lineno)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    u.logmsg('[OK]  read_history')



def read_system_information(modbus):    
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)
    if not r.exists(im.RK_SYS_INFO + str(glb.DEVICE_ID)):
        response = modbus.read_holding_registers(address=sr.addr_retedChargingCurrent, count=1, slave=glb.DEVICE_ID)
        maxSupportVoltage = response.registers[0] >> 8 
        retedChargingCurrent = response.registers[0] & 0x00FF

        response = modbus.read_holding_registers(address=sr.addr_ratedDischargeCurrent, count=1, slave=glb.DEVICE_ID)
        ratedDischargeCurrent = response.registers[0] >> 8
        deviceType = glb.DEVICE_TYPE_INVERTER if response.registers[0] & 0x00FF else glb.DEVICE_TYPE_CONTROLLER
        
        model = ''
        response = modbus.read_holding_registers(address=sr.addr_model, count=8, slave=glb.DEVICE_ID)
        for ch in response.registers:
            hi = ch >> 8
            lo = ch & 0x00FF
            model += chr(hi) + chr(lo)
        
        softwareVersion = ''
        response = modbus.read_holding_registers(address=sr.addr_softwareVersion, count=2, slave=glb.DEVICE_ID)
        for ch in response.registers:
            hi = ch >> 8
            lo = ch & 0x00FF
            softwareVersion += '.' + str(hi) + '.' + str(lo)
        softwareVersion = softwareVersion[1:]

        hardwareVersion = ''
        response = modbus.read_holding_registers(address=sr.addr_hardwareVersion, count=2, slave=glb.DEVICE_ID)
        for ch in response.registers:
            hi = ch >> 8
            lo = ch & 0x00FF
            hardwareVersion += '.' + str(hi) + '.' + str(lo)
        hardwareVersion = hardwareVersion[1:]

        serialNumber = ''
        response = modbus.read_holding_registers(address=sr.addr_serialNumber, count=2, slave=glb.DEVICE_ID)
        for ch in response.registers:
            hi = ch >> 8
            lo = ch &  0x00FF
            serialNumber += str(hi) + str(lo)


        system_information = [
            { 'maxSupportVoltage': maxSupportVoltage, 'unit': glb.UNIT_VOLT },
            { 'retedChargingCurrent': retedChargingCurrent, 'unit': glb.UNIT_AMPERE},
            { 'ratedDischargeCurrent': ratedDischargeCurrent, 'unit': glb.UNIT_AMPERE},
            { 'deviceType': deviceType, 'unit': glb.UNIT_STRING},
            { 'model': model, 'unit': glb.UNIT_STRING},
            { 'softwareVersion': softwareVersion, 'unit': glb.UNIT_STRING},
            { 'hardwareVersion': hardwareVersion, 'unit': glb.UNIT_STRING},
            { 'serialNumber': serialNumber, 'unit': glb.UNIT_STRING},
        ]

        sys_info_text = json.dumps(system_information)
        r.set(im.RK_SYS_INFO + str(glb.DEVICE_ID), sys_info_text)

        if glb.PUBLISH_BROKER_ENABLED:
            br.publish(br.TOPIC_SYS_INFO, sys_info_text)
        
        try:
            conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO device.system_information(payload, device_id) 
                VALUES (%s,%s);
            """
            cursor.execute(insert_query, (sys_info_text, glb.DEVICE_ID,))
            conn.commit()            
        except Exception as e:
            #print(f"An error occurred: {e}")
            print(f"Error occurred: {type(e).__name__}: {e}")
            print("Line number:", traceback.extract_tb(e.__traceback__)[-1].lineno)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        u.logmsg('system_information updated')

    u.logmsg('[OK]  read_system_information')



def read_register(modbus, addr):
    response = modbus.read_holding_registers(address=addr, count=1, slave=glb.DEVICE_ID)
    return response.registers[0]



def read_controller_settings(modbus):
    # # over Voltage Threshold
    # print(read_register(modbus, 0xE005))
    # # Charging voltage limit
    # print(read_register(modbus, 0xE006))
    # print(read_register(modbus, 0xE007))
    # print(read_register(modbus, 0xE008))
    # # Floating charging voltage/ overcharge recovery voltage (lithium batteries)
    # print(read_register(modbus, 0xE009))

    # #Boost charging recovery voltage
    # print(read_register(modbus, 0xE00A))
    # print(read_register(modbus, 0xE00B))
    # print(read_register(modbus, 0xE00C))
    # print(read_register(modbus, 0xE00D))
    # print(read_register(modbus, 0xE00E))
    
    # # Over-discharge time delay
    # print(read_register(modbus, 0xE010))
    # print(read_register(modbus, 0xE011))
    # print(read_register(modbus, 0xE012))
    # print(read_register(modbus, 0xE013))
    # # Temperature compensation factor
    # print(read_register(modbus, 0xE014))

    
    r = redis.StrictRedis(host=glb.REDIS_ADDR, port=glb.REDIS_PORT, db=0)

    need_to_update = False
    if not r.exists(im.RK_SETTINGS + str(glb.DEVICE_ID)):
        need_to_update = True
    else:        
        if r.get(im.RK_SETTINGS + str(glb.DEVICE_ID)) == '':
            need_to_update = True
    
    if need_to_update:
        reg = read_register(modbus, sr.addr_specialPowerControl)

        settings = {
            'common': [
                {'boostchargingRecoveryVoltage': read_register(modbus, sr.addr_boostchargingRecoveryVoltage), 'unit': glb.UNIT_VOLT },
                {'overDischargeRecoveryVoltage': read_register(modbus, sr.addr_overDischargeRecoveryVoltage), 'unit': glb.UNIT_VOLT },
                {'underVoltageWarningLevel': read_register(modbus, sr.addr_underVoltageWarningLevel), 'unit': glb.UNIT_VOLT },
                {'overDischargeVoltage': read_register(modbus, sr.addr_overDischargeVoltage), 'unit': glb.UNIT_VOLT },
                {'dischargingLimitVoltage': read_register(modbus, sr.addr_dischargingLimitVoltage), 'unit': glb.UNIT_VOLT },
                {'overDischareTimeDelay': read_register(modbus, sr.addr_overDischareTimeDelay), 'unit': glb.UNIT_SECOND },
                {'equalizingChargingTime': read_register(modbus, sr.addr_equalizingChargingTime), 'unit': glb.UNIT_MINUTE },
                {'boostChargingTime': read_register(modbus, sr.addr_boostChargingTime), 'unit': glb.UNIT_MINUTE },
                {'equalizingChargingInterval': read_register(modbus, sr.addr_equalizingChargingInterval), 'unit': glb.UNIT_DAY },
                {'temperatureCompensationFactor': read_register(modbus, sr.addr_temperatureCompensationFactor), 'unit': glb.UNIT_MV },
                {'loadWorkingMode': glb.workingModes[read_register(modbus, sr.addr_loadWorkingMode)], 'unit': glb.UNIT_STRING },
            ],
            'battery': [
                {'nominalBatteryCapacity': read_register(modbus, sr.addr_nominalBatteryCapacity),  'unit': glb.UNIT_AH },
                {'systemVoltageSetting': read_register(modbus, sr.addr_systemVoltageSetting) >> 8, 'unit': glb.UNIT_VOLT },
                {'recognizedVoltage': read_register(modbus, sr.addr_batteryType) & 0x00FF, 'unit': glb.UNIT_VOLT },
                {'batteryType': glb.batteryTypes[read_register(modbus, sr.addr_batteryType)], 'unit': glb.UNIT_STRING },
                {'overVoltageThreshold': read_register(modbus, sr.addr_overVoltageThreshold), 'unit': glb.UNIT_VOLT },
                {'chargingVoltageLimit': read_register(modbus, sr.addr_chargingVoltageLimit), 'unit': glb.UNIT_VOLT },
                {'equalizingChargingVoltage': read_register(modbus, sr.addr_equalizingChargingVoltage), 'unit': glb.UNIT_VOLT },
                {'boostchargingVoltage': read_register(modbus, sr.addr_boostchargingVoltage), 'unit': glb.UNIT_VOLT },
                {'floatingChargingVoltage': read_register(modbus, sr.addr_floatingChargingVoltage), 'unit': glb.UNIT_VOLT }
            ],
            'lightControl': {
                'common': [
                    {'lightControlDelay': read_register(modbus, sr.addr_lightControlDelay), 'unit': glb.UNIT_MINUTE },
                    {'lightControlVoltage': read_register(modbus, sr.addr_lightControlVoltage), 'unit': glb.UNIT_VOLT }
                ],
                'specialPowerControl': [
                    {'eachNightOnFunctionEnabled': True if (reg >> 8) & 0x01 else False, 'unit': glb.UNIT_VOLT },
                    {'specialPowerControlFunctionEnabled': True if (reg >> 9) & 0x01 else False, 'unit': glb.UNIT_VOLT },
                    {'noChargingBelowZero': True if (reg & 0x0008) >> 2 else False, 'unit': glb.UNIT_VOLT },
                    {'charging method': 'PWM charging' if (reg >> 9) & 0x0003 else 'direct charging', 'unit': glb.UNIT_VOLT }
                ]
            }
        }
        
        settings_text = json.dumps(settings)

        r.set(im.RK_SETTINGS + str(glb.DEVICE_ID), settings_text)
        
        if glb.PUBLISH_BROKER_ENABLED:
            br.publish(br.TOPIC_SETTINGS, settings_text)

        try:
            conn = psycopg2.connect(**glb.PG_CONNECT_PARAMS)
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO device.eeprom_parameter_setting(payload, device_id) 
                VALUES (%s,%s);
            """
            cursor.execute(insert_query, (settings_text, glb.DEVICE_ID,))
            conn.commit()            
        except Exception as e:        
            print(f"Error occurred: {type(e).__name__}: {e}")
            print("Line number:", traceback.extract_tb(e.__traceback__)[-1].lineno)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    u.logmsg('[OK]  read_controller_settings')




