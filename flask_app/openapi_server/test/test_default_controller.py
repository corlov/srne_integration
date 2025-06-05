import unittest

from flask import json

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_name_get(self):
        """Test case for name_get

        
        """
        query_string = [('deviceId', 56)]
        headers = { 
        }
        response = self.client.open(
            '/v1/name',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
