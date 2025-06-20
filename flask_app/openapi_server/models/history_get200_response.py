from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.history_get200_response_message import HistoryGet200ResponseMessage
from openapi_server import util

from openapi_server.models.history_get200_response_message import HistoryGet200ResponseMessage  # noqa: E501

class HistoryGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None):  # noqa: E501
        """HistoryGet200Response - a model defined in OpenAPI

        :param message: The message of this HistoryGet200Response.  # noqa: E501
        :type message: HistoryGet200ResponseMessage
        """
        self.openapi_types = {
            'message': HistoryGet200ResponseMessage
        }

        self.attribute_map = {
            'message': 'message'
        }

        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'HistoryGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _history_get_200_response of this HistoryGet200Response.  # noqa: E501
        :rtype: HistoryGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self) -> HistoryGet200ResponseMessage:
        """Gets the message of this HistoryGet200Response.


        :return: The message of this HistoryGet200Response.
        :rtype: HistoryGet200ResponseMessage
        """
        return self._message

    @message.setter
    def message(self, message: HistoryGet200ResponseMessage):
        """Sets the message of this HistoryGet200Response.


        :param message: The message of this HistoryGet200Response.
        :type message: HistoryGet200ResponseMessage
        """

        self._message = message
