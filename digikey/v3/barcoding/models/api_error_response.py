# coding: utf-8

"""
    Barcoding

    Retrieve package information from the barcode.  # noqa: E501

    OpenAPI spec version: v3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from digikey.v3.barcoding.configuration import Configuration


class ApiErrorResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'error_response_version': 'str',
        'status_code': 'int',
        'error_message': 'str',
        'error_details': 'str',
        'request_id': 'str',
        'validation_errors': 'list[ApiValidationError]'
    }

    attribute_map = {
        'error_response_version': 'ErrorResponseVersion',
        'status_code': 'StatusCode',
        'error_message': 'ErrorMessage',
        'error_details': 'ErrorDetails',
        'request_id': 'RequestId',
        'validation_errors': 'ValidationErrors'
    }

    def __init__(self, error_response_version=None, status_code=None, error_message=None, error_details=None, request_id=None, validation_errors=None, _configuration=None):  # noqa: E501
        """ApiErrorResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._error_response_version = None
        self._status_code = None
        self._error_message = None
        self._error_details = None
        self._request_id = None
        self._validation_errors = None
        self.discriminator = None

        if error_response_version is not None:
            self.error_response_version = error_response_version
        if status_code is not None:
            self.status_code = status_code
        if error_message is not None:
            self.error_message = error_message
        if error_details is not None:
            self.error_details = error_details
        if request_id is not None:
            self.request_id = request_id
        if validation_errors is not None:
            self.validation_errors = validation_errors

    @property
    def error_response_version(self):
        """Gets the error_response_version of this ApiErrorResponse.  # noqa: E501


        :return: The error_response_version of this ApiErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._error_response_version

    @error_response_version.setter
    def error_response_version(self, error_response_version):
        """Sets the error_response_version of this ApiErrorResponse.


        :param error_response_version: The error_response_version of this ApiErrorResponse.  # noqa: E501
        :type: str
        """

        self._error_response_version = error_response_version

    @property
    def status_code(self):
        """Gets the status_code of this ApiErrorResponse.  # noqa: E501


        :return: The status_code of this ApiErrorResponse.  # noqa: E501
        :rtype: int
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """Sets the status_code of this ApiErrorResponse.


        :param status_code: The status_code of this ApiErrorResponse.  # noqa: E501
        :type: int
        """

        self._status_code = status_code

    @property
    def error_message(self):
        """Gets the error_message of this ApiErrorResponse.  # noqa: E501


        :return: The error_message of this ApiErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this ApiErrorResponse.


        :param error_message: The error_message of this ApiErrorResponse.  # noqa: E501
        :type: str
        """

        self._error_message = error_message

    @property
    def error_details(self):
        """Gets the error_details of this ApiErrorResponse.  # noqa: E501


        :return: The error_details of this ApiErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._error_details

    @error_details.setter
    def error_details(self, error_details):
        """Sets the error_details of this ApiErrorResponse.


        :param error_details: The error_details of this ApiErrorResponse.  # noqa: E501
        :type: str
        """

        self._error_details = error_details

    @property
    def request_id(self):
        """Gets the request_id of this ApiErrorResponse.  # noqa: E501


        :return: The request_id of this ApiErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this ApiErrorResponse.


        :param request_id: The request_id of this ApiErrorResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def validation_errors(self):
        """Gets the validation_errors of this ApiErrorResponse.  # noqa: E501


        :return: The validation_errors of this ApiErrorResponse.  # noqa: E501
        :rtype: list[ApiValidationError]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """Sets the validation_errors of this ApiErrorResponse.


        :param validation_errors: The validation_errors of this ApiErrorResponse.  # noqa: E501
        :type: list[ApiValidationError]
        """

        self._validation_errors = validation_errors

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ApiErrorResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiErrorResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApiErrorResponse):
            return True

        return self.to_dict() != other.to_dict()
