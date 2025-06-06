import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.clear_history_post200_response import ClearHistoryPost200Response  # noqa: E501
from openapi_server.models.dynamic_data_get200_response import DynamicDataGet200Response  # noqa: E501
from openapi_server.models.history_get200_response import HistoryGet200Response  # noqa: E501
from openapi_server.models.settings_get200_response import SettingsGet200Response  # noqa: E501
from openapi_server.models.system_info_get200_response import SystemInfoGet200Response  # noqa: E501
from openapi_server import util

import time
import redis
import json
from datetime import datetime
import uuid
import os


REDIS_ADDR = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

RK_TELEMETRY = 'telemetry'
RK_SYS_INFO = 'system_information'
RK_SETTINGS = 'eeprom_parameter_setting'
RK_COMMAND = 'command'
RK_HISTORY = 'history'
RK_COMMAND_RESPONSE = 'commands_responses'


def redis_read(key_name, device_id, additonal_params=""):
    r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)
    
    key = key_name + str(device_id) + additonal_params
    payload = ''
    if r.exists(key):
        payload = r.get(key)
        return json.loads(payload)

    return ''
    


def cmd_body(command_name):
    now = datetime.now()    

    cmd = {}
    #TODO: авторизацию на распбери надо сделать хотя бы basic
    cmd['user'] = 'admin'
    cmd['command'] = command_name
    cmd['created_at'] = str(now.timestamp())
    cmd['uuid'] = str(uuid.uuid4())

    return cmd


def send_command(cmd, device_id):
    r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

    print("\n\n" + json.dumps(cmd) + "\n\n")

    r.set('command' + str(device_id), json.dumps(cmd))

    # TODO: затем в асинхроне спросить результат команды это должен сделать бекенд
    response = {}
    response['uuid'] = str(cmd['uuid'])

    return json.dumps(response)





def clear_history_post(device_id):  # noqa: E501
    """clear_history_post

    очистить всю историю на устройстве (флеш память) # noqa: E501

    :param device_id: id устройства
    :type device_id: int

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """

    cmd = cmd_body('clear_history')
    return json.loads(send_command(cmd, device_id))



def control_load_on_off_post(device_id, on):  # noqa: E501
    """control_load_on_off_post

    включить или выкл. нагрузку запитаную от АКБ # noqa: E501

    :param device_id: id устройства
    :type device_id: int
    :param on: вкл &#x3D; ИСТИНА, выкл &#x3D; ЛОЖЬ
    :type on: bool

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """
    
    cmd = cmd_body('control_load_on_off')
    cmd['value'] = on
    return json.loads(send_command(cmd, device_id))



def dynamic_data_get(device_id):  # noqa: E501
    """dynamic_data_get

    текущее состояние параметров контроллера # noqa: E501

    :param device_id: id устройства
    :type device_id: int

    :rtype: Union[DynamicDataGet200Response, Tuple[DynamicDataGet200Response, int], Tuple[DynamicDataGet200Response, int, Dict[str, str]]
    """
    return redis_read(RK_TELEMETRY, device_id)


def history_get(device_id, date):  # noqa: E501
    """history_get

    история за определенную дату # noqa: E501

    :param device_id: id устройства
    :type device_id: int
    :param _date: За какую дату отдать значения параметров
    :type _date: str

    :rtype: Union[HistoryGet200Response, Tuple[HistoryGet200Response, int], Tuple[HistoryGet200Response, int, Dict[str, str]]
    """

    return redis_read(RK_HISTORY, device_id, '_' + date)


def reset_to_factory_default_settings_post(device_id):  # noqa: E501
    """reset_to_factory_default_settings_post

    Сброс всех настроек в по-умолчанию зашитых производителем # noqa: E501

    :param device_id: id устройства
    :type device_id: int

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """
    
    cmd = cmd_body('reset_to_factory_default_settings')
    return json.loads(send_command(cmd, device_id))


def set_charge_current_post(device_id, current_value):  # noqa: E501
    """set_charge_current_post

    установка тока зарядки # noqa: E501

    :param device_id: id устройства
    :type device_id: int
    :param current_value: значения силы тока в амперах (A general rule of thumb is to use a charging current of around 10% of the battery&#39;s capacity for optimal and safe charging. For example, a 50 Ah battery would ideally be charged with a current of around 5 amps. )
    :type current_value: 

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """
    cmd = cmd_body('set_charge_current')
    cmd['value'] = float(current_value)
    return json.loads(send_command(cmd, device_id))


def set_load_working_mode_post(device_id, mode_code):  # noqa: E501
    """set_load_working_mode_post

    Режим работы устройства # noqa: E501

    :param device_id: id устройства
    :type device_id: int
    :param mode_code: значенияч от 0 до 17 включительно (18 режимов всего)
    :type mode_code: int

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """
    cmd = cmd_body('set_load_working_mode')
    cmd['value'] = int(mode_code)
    return json.loads(send_command(cmd, device_id))


def set_parameters_post(device_id, over_voltage_threshold, charging_limit_voltage, equalizing_charging_voltage, boost_charging_voltage, floating_charging_voltage, boost_charging_recovery, over_discharge_recovery, under_voltage_threshold, over_discharge_voltage, over_discharge_limit_voltage, end_of_charge_and_discharge_capacity, over_discharge_time_delay, equalizing_charging_time, boost_charging_time, equalizing_charging_interval, temperature_compensation):  # noqa: E501
    """set_parameters_post

    Установка параметров работы устройства # noqa: E501

    :param device_id: id устройства
    :type device_id: int
    :param over_voltage_threshold: 
    :type over_voltage_threshold: 
    :param charging_limit_voltage: 
    :type charging_limit_voltage: 
    :param equalizing_charging_voltage: 
    :type equalizing_charging_voltage: 
    :param boost_charging_voltage: 
    :type boost_charging_voltage: 
    :param floating_charging_voltage: 
    :type floating_charging_voltage: 
    :param boost_charging_recovery: 
    :type boost_charging_recovery: 
    :param over_discharge_recovery: 
    :type over_discharge_recovery: 
    :param under_voltage_threshold: 
    :type under_voltage_threshold: 
    :param over_discharge_voltage: 
    :type over_discharge_voltage: 
    :param over_discharge_limit_voltage: 
    :type over_discharge_limit_voltage: int
    :param end_of_charge_and_discharge_capacity: 
    :type end_of_charge_and_discharge_capacity: int
    :param over_discharge_time_delay: 
    :type over_discharge_time_delay: int
    :param equalizing_charging_time: 
    :type equalizing_charging_time: int
    :param boost_charging_time: 
    :type boost_charging_time: int
    :param equalizing_charging_interval: 
    :type equalizing_charging_interval: int
    :param temperature_compensation: 
    :type temperature_compensation: int

    :rtype: Union[ClearHistoryPost200Response, Tuple[ClearHistoryPost200Response, int], Tuple[ClearHistoryPost200Response, int, Dict[str, str]]
    """

    parameters = [over_voltage_threshold, charging_limit_voltage, equalizing_charging_voltage, boost_charging_voltage, floating_charging_voltage, boost_charging_recovery, over_discharge_recovery, under_voltage_threshold, over_discharge_voltage, over_discharge_limit_voltage, end_of_charge_and_discharge_capacity, over_discharge_time_delay, equalizing_charging_time, boost_charging_time, equalizing_charging_interval, temperature_compensation]
    cmd = cmd_body('set_parameters')
    cmd['parameters'] = parameters
    return json.loads(send_command(cmd, device_id))



def command_status_get(uuid):  # noqa: E501
    """command_status_get

    Асинхронно получить статус отправленной ранее команды # noqa: E501

    :param uuid: uuid отправленной ранее команды
    :type uuid: str

    :rtype: Union[CommandStatusGet200Response, Tuple[CommandStatusGet200Response, int], Tuple[CommandStatusGet200Response, int, Dict[str, str]]
    """

    r = redis.StrictRedis(host=REDIS_ADDR, port=REDIS_PORT, db=0)

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

    for cmd in fresh_commands:
        if uuid == cmd['uuid']:
            target_response = cmd

    # Обновляем список ответов, удалив протухшие ответы по времени
    r.delete(RK_COMMAND_RESPONSE)
    for cmd in fresh_commands:
        r.rpush(RK_COMMAND_RESPONSE, json.dumps(cmd))

    
    return target_response



def settings_get(device_id):  # noqa: E501
    """settings_get

    считать текущие настройки # noqa: E501

    :param device_id: id устройства
    :type device_id: int

    :rtype: Union[SettingsGet200Response, Tuple[SettingsGet200Response, int], Tuple[SettingsGet200Response, int, Dict[str, str]]
    """
    return redis_read(RK_SETTINGS, device_id)


def system_info_get(device_id):  # noqa: E501
    """system_info_get

    System information # noqa: E501

    :param device_id: id устройства
    :type device_id: int

    :rtype: Union[SystemInfoGet200Response, Tuple[SystemInfoGet200Response, int], Tuple[SystemInfoGet200Response, int, Dict[str, str]]
    """    
    return redis_read(RK_SYS_INFO, device_id)

