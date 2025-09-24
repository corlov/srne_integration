import unittest

from flask import json

from openapi_server.models.clear_history_post200_response import ClearHistoryPost200Response  # noqa: E501
from openapi_server.models.command_status_get200_response import CommandStatusGet200Response  # noqa: E501
from openapi_server.models.dynamic_data_get200_response import DynamicDataGet200Response  # noqa: E501
from openapi_server.models.history_get200_response import HistoryGet200Response  # noqa: E501
from openapi_server.models.settings_get200_response import SettingsGet200Response  # noqa: E501
from openapi_server.models.system_info_get200_response import SystemInfoGet200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_clear_history_post(self):
        """Test case for clear_history_post

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/clear_history',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_command_status_get(self):
        """Test case for command_status_get

        
        """
        query_string = [('uuid', 'uuid_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/command_status',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_control_load_on_off_post(self):
        """Test case for control_load_on_off_post

        
        """
        query_string = [('deviceId', 56),
                        ('on', True)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/control_load_on_off',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_dynamic_data_get(self):
        """Test case for dynamic_data_get

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/dynamic_data',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_history_get(self):
        """Test case for history_get

        
        """
        query_string = [('deviceId', 56),
                        ('date', '_date_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/history',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset_to_factory_default_settings_post(self):
        """Test case for reset_to_factory_default_settings_post

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/reset_to_factory_default_settings',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_charge_current_post(self):
        """Test case for set_charge_current_post

        
        """
        query_string = [('deviceId', 56),
                        ('currentValue', 0.45)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/set_charge_current',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_load_working_mode_post(self):
        """Test case for set_load_working_mode_post

        
        """
        query_string = [('deviceId', 56),
                        ('modeCode', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/set_load_working_mode',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_parameters_post(self):
        """Test case for set_parameters_post

        
        """
        query_string = [('deviceId', 56),
                        ('overVoltageThreshold', 3.4),
                        ('chargingLimitVoltage', 3.4),
                        ('equalizingChargingVoltage', 3.4),
                        ('boostChargingVoltage', 3.4),
                        ('floatingChargingVoltage', 3.4),
                        ('boostChargingRecovery', 3.4),
                        ('overDischargeRecovery', 3.4),
                        ('underVoltageThreshold', 3.4),
                        ('overDischargeVoltage', 3.4),
                        ('overDischargeLimitVoltage', 56),
                        ('endOfChargeAndDischargeCapacity', 56),
                        ('overDischargeTimeDelay', 56),
                        ('equalizingChargingTime', 56),
                        ('boostChargingTime', 56),
                        ('equalizingChargingInterval', 56),
                        ('temperatureCompensation', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/set_parameters',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_settings_get(self):
        """Test case for settings_get

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/settings',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_system_info_get(self):
        """Test case for system_info_get

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/system_info',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
