from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.settings_get200_response_message_battery import SettingsGet200ResponseMessageBattery
from openapi_server.models.settings_get200_response_message_light_control import SettingsGet200ResponseMessageLightControl
from openapi_server import util

from openapi_server.models.settings_get200_response_message_battery import SettingsGet200ResponseMessageBattery  # noqa: E501
from openapi_server.models.settings_get200_response_message_light_control import SettingsGet200ResponseMessageLightControl  # noqa: E501

class SettingsGet200ResponseMessage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, load_working_mode=None, boost_charging_time=None, over_discharge_voltage=None, over_dischare_time_delay=None, equalizing_charging_time=None, discharging_limit_voltage=None, under_voltage_warning_level=None, boostcharging_recovery_voltage=None, equalizing_charging_interval=None, over_discharge_recovery_voltage=None, temperature_compensation_factor=None, light_control=None, battery=None):  # noqa: E501
        """SettingsGet200ResponseMessage - a model defined in OpenAPI

        :param load_working_mode: The load_working_mode of this SettingsGet200ResponseMessage.  # noqa: E501
        :type load_working_mode: str
        :param boost_charging_time: The boost_charging_time of this SettingsGet200ResponseMessage.  # noqa: E501
        :type boost_charging_time: int
        :param over_discharge_voltage: The over_discharge_voltage of this SettingsGet200ResponseMessage.  # noqa: E501
        :type over_discharge_voltage: int
        :param over_dischare_time_delay: The over_dischare_time_delay of this SettingsGet200ResponseMessage.  # noqa: E501
        :type over_dischare_time_delay: int
        :param equalizing_charging_time: The equalizing_charging_time of this SettingsGet200ResponseMessage.  # noqa: E501
        :type equalizing_charging_time: int
        :param discharging_limit_voltage: The discharging_limit_voltage of this SettingsGet200ResponseMessage.  # noqa: E501
        :type discharging_limit_voltage: int
        :param under_voltage_warning_level: The under_voltage_warning_level of this SettingsGet200ResponseMessage.  # noqa: E501
        :type under_voltage_warning_level: int
        :param boostcharging_recovery_voltage: The boostcharging_recovery_voltage of this SettingsGet200ResponseMessage.  # noqa: E501
        :type boostcharging_recovery_voltage: int
        :param equalizing_charging_interval: The equalizing_charging_interval of this SettingsGet200ResponseMessage.  # noqa: E501
        :type equalizing_charging_interval: int
        :param over_discharge_recovery_voltage: The over_discharge_recovery_voltage of this SettingsGet200ResponseMessage.  # noqa: E501
        :type over_discharge_recovery_voltage: int
        :param temperature_compensation_factor: The temperature_compensation_factor of this SettingsGet200ResponseMessage.  # noqa: E501
        :type temperature_compensation_factor: int
        :param light_control: The light_control of this SettingsGet200ResponseMessage.  # noqa: E501
        :type light_control: SettingsGet200ResponseMessageLightControl
        :param battery: The battery of this SettingsGet200ResponseMessage.  # noqa: E501
        :type battery: SettingsGet200ResponseMessageBattery
        """
        self.openapi_types = {
            'load_working_mode': str,
            'boost_charging_time': int,
            'over_discharge_voltage': int,
            'over_dischare_time_delay': int,
            'equalizing_charging_time': int,
            'discharging_limit_voltage': int,
            'under_voltage_warning_level': int,
            'boostcharging_recovery_voltage': int,
            'equalizing_charging_interval': int,
            'over_discharge_recovery_voltage': int,
            'temperature_compensation_factor': int,
            'light_control': SettingsGet200ResponseMessageLightControl,
            'battery': SettingsGet200ResponseMessageBattery
        }

        self.attribute_map = {
            'load_working_mode': 'loadWorkingMode',
            'boost_charging_time': 'boostChargingTime',
            'over_discharge_voltage': 'overDischargeVoltage',
            'over_dischare_time_delay': 'overDischareTimeDelay',
            'equalizing_charging_time': 'equalizingChargingTime',
            'discharging_limit_voltage': 'dischargingLimitVoltage',
            'under_voltage_warning_level': 'underVoltageWarningLevel',
            'boostcharging_recovery_voltage': 'boostchargingRecoveryVoltage',
            'equalizing_charging_interval': 'equalizingChargingInterval',
            'over_discharge_recovery_voltage': 'overDischargeRecoveryVoltage',
            'temperature_compensation_factor': 'temperatureCompensationFactor',
            'light_control': 'lightControl',
            'battery': 'battery'
        }

        self._load_working_mode = load_working_mode
        self._boost_charging_time = boost_charging_time
        self._over_discharge_voltage = over_discharge_voltage
        self._over_dischare_time_delay = over_dischare_time_delay
        self._equalizing_charging_time = equalizing_charging_time
        self._discharging_limit_voltage = discharging_limit_voltage
        self._under_voltage_warning_level = under_voltage_warning_level
        self._boostcharging_recovery_voltage = boostcharging_recovery_voltage
        self._equalizing_charging_interval = equalizing_charging_interval
        self._over_discharge_recovery_voltage = over_discharge_recovery_voltage
        self._temperature_compensation_factor = temperature_compensation_factor
        self._light_control = light_control
        self._battery = battery

    @classmethod
    def from_dict(cls, dikt) -> 'SettingsGet200ResponseMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _settings_get_200_response_message of this SettingsGet200ResponseMessage.  # noqa: E501
        :rtype: SettingsGet200ResponseMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def load_working_mode(self) -> str:
        """Gets the load_working_mode of this SettingsGet200ResponseMessage.


        :return: The load_working_mode of this SettingsGet200ResponseMessage.
        :rtype: str
        """
        return self._load_working_mode

    @load_working_mode.setter
    def load_working_mode(self, load_working_mode: str):
        """Sets the load_working_mode of this SettingsGet200ResponseMessage.


        :param load_working_mode: The load_working_mode of this SettingsGet200ResponseMessage.
        :type load_working_mode: str
        """

        self._load_working_mode = load_working_mode

    @property
    def boost_charging_time(self) -> int:
        """Gets the boost_charging_time of this SettingsGet200ResponseMessage.


        :return: The boost_charging_time of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._boost_charging_time

    @boost_charging_time.setter
    def boost_charging_time(self, boost_charging_time: int):
        """Sets the boost_charging_time of this SettingsGet200ResponseMessage.


        :param boost_charging_time: The boost_charging_time of this SettingsGet200ResponseMessage.
        :type boost_charging_time: int
        """

        self._boost_charging_time = boost_charging_time

    @property
    def over_discharge_voltage(self) -> int:
        """Gets the over_discharge_voltage of this SettingsGet200ResponseMessage.


        :return: The over_discharge_voltage of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._over_discharge_voltage

    @over_discharge_voltage.setter
    def over_discharge_voltage(self, over_discharge_voltage: int):
        """Sets the over_discharge_voltage of this SettingsGet200ResponseMessage.


        :param over_discharge_voltage: The over_discharge_voltage of this SettingsGet200ResponseMessage.
        :type over_discharge_voltage: int
        """

        self._over_discharge_voltage = over_discharge_voltage

    @property
    def over_dischare_time_delay(self) -> int:
        """Gets the over_dischare_time_delay of this SettingsGet200ResponseMessage.


        :return: The over_dischare_time_delay of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._over_dischare_time_delay

    @over_dischare_time_delay.setter
    def over_dischare_time_delay(self, over_dischare_time_delay: int):
        """Sets the over_dischare_time_delay of this SettingsGet200ResponseMessage.


        :param over_dischare_time_delay: The over_dischare_time_delay of this SettingsGet200ResponseMessage.
        :type over_dischare_time_delay: int
        """

        self._over_dischare_time_delay = over_dischare_time_delay

    @property
    def equalizing_charging_time(self) -> int:
        """Gets the equalizing_charging_time of this SettingsGet200ResponseMessage.


        :return: The equalizing_charging_time of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._equalizing_charging_time

    @equalizing_charging_time.setter
    def equalizing_charging_time(self, equalizing_charging_time: int):
        """Sets the equalizing_charging_time of this SettingsGet200ResponseMessage.


        :param equalizing_charging_time: The equalizing_charging_time of this SettingsGet200ResponseMessage.
        :type equalizing_charging_time: int
        """

        self._equalizing_charging_time = equalizing_charging_time

    @property
    def discharging_limit_voltage(self) -> int:
        """Gets the discharging_limit_voltage of this SettingsGet200ResponseMessage.


        :return: The discharging_limit_voltage of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._discharging_limit_voltage

    @discharging_limit_voltage.setter
    def discharging_limit_voltage(self, discharging_limit_voltage: int):
        """Sets the discharging_limit_voltage of this SettingsGet200ResponseMessage.


        :param discharging_limit_voltage: The discharging_limit_voltage of this SettingsGet200ResponseMessage.
        :type discharging_limit_voltage: int
        """

        self._discharging_limit_voltage = discharging_limit_voltage

    @property
    def under_voltage_warning_level(self) -> int:
        """Gets the under_voltage_warning_level of this SettingsGet200ResponseMessage.


        :return: The under_voltage_warning_level of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._under_voltage_warning_level

    @under_voltage_warning_level.setter
    def under_voltage_warning_level(self, under_voltage_warning_level: int):
        """Sets the under_voltage_warning_level of this SettingsGet200ResponseMessage.


        :param under_voltage_warning_level: The under_voltage_warning_level of this SettingsGet200ResponseMessage.
        :type under_voltage_warning_level: int
        """

        self._under_voltage_warning_level = under_voltage_warning_level

    @property
    def boostcharging_recovery_voltage(self) -> int:
        """Gets the boostcharging_recovery_voltage of this SettingsGet200ResponseMessage.


        :return: The boostcharging_recovery_voltage of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._boostcharging_recovery_voltage

    @boostcharging_recovery_voltage.setter
    def boostcharging_recovery_voltage(self, boostcharging_recovery_voltage: int):
        """Sets the boostcharging_recovery_voltage of this SettingsGet200ResponseMessage.


        :param boostcharging_recovery_voltage: The boostcharging_recovery_voltage of this SettingsGet200ResponseMessage.
        :type boostcharging_recovery_voltage: int
        """

        self._boostcharging_recovery_voltage = boostcharging_recovery_voltage

    @property
    def equalizing_charging_interval(self) -> int:
        """Gets the equalizing_charging_interval of this SettingsGet200ResponseMessage.


        :return: The equalizing_charging_interval of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._equalizing_charging_interval

    @equalizing_charging_interval.setter
    def equalizing_charging_interval(self, equalizing_charging_interval: int):
        """Sets the equalizing_charging_interval of this SettingsGet200ResponseMessage.


        :param equalizing_charging_interval: The equalizing_charging_interval of this SettingsGet200ResponseMessage.
        :type equalizing_charging_interval: int
        """

        self._equalizing_charging_interval = equalizing_charging_interval

    @property
    def over_discharge_recovery_voltage(self) -> int:
        """Gets the over_discharge_recovery_voltage of this SettingsGet200ResponseMessage.


        :return: The over_discharge_recovery_voltage of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._over_discharge_recovery_voltage

    @over_discharge_recovery_voltage.setter
    def over_discharge_recovery_voltage(self, over_discharge_recovery_voltage: int):
        """Sets the over_discharge_recovery_voltage of this SettingsGet200ResponseMessage.


        :param over_discharge_recovery_voltage: The over_discharge_recovery_voltage of this SettingsGet200ResponseMessage.
        :type over_discharge_recovery_voltage: int
        """

        self._over_discharge_recovery_voltage = over_discharge_recovery_voltage

    @property
    def temperature_compensation_factor(self) -> int:
        """Gets the temperature_compensation_factor of this SettingsGet200ResponseMessage.


        :return: The temperature_compensation_factor of this SettingsGet200ResponseMessage.
        :rtype: int
        """
        return self._temperature_compensation_factor

    @temperature_compensation_factor.setter
    def temperature_compensation_factor(self, temperature_compensation_factor: int):
        """Sets the temperature_compensation_factor of this SettingsGet200ResponseMessage.


        :param temperature_compensation_factor: The temperature_compensation_factor of this SettingsGet200ResponseMessage.
        :type temperature_compensation_factor: int
        """

        self._temperature_compensation_factor = temperature_compensation_factor

    @property
    def light_control(self) -> SettingsGet200ResponseMessageLightControl:
        """Gets the light_control of this SettingsGet200ResponseMessage.


        :return: The light_control of this SettingsGet200ResponseMessage.
        :rtype: SettingsGet200ResponseMessageLightControl
        """
        return self._light_control

    @light_control.setter
    def light_control(self, light_control: SettingsGet200ResponseMessageLightControl):
        """Sets the light_control of this SettingsGet200ResponseMessage.


        :param light_control: The light_control of this SettingsGet200ResponseMessage.
        :type light_control: SettingsGet200ResponseMessageLightControl
        """

        self._light_control = light_control

    @property
    def battery(self) -> SettingsGet200ResponseMessageBattery:
        """Gets the battery of this SettingsGet200ResponseMessage.


        :return: The battery of this SettingsGet200ResponseMessage.
        :rtype: SettingsGet200ResponseMessageBattery
        """
        return self._battery

    @battery.setter
    def battery(self, battery: SettingsGet200ResponseMessageBattery):
        """Sets the battery of this SettingsGet200ResponseMessage.


        :param battery: The battery of this SettingsGet200ResponseMessage.
        :type battery: SettingsGet200ResponseMessageBattery
        """

        self._battery = battery
