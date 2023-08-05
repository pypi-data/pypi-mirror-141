# coding: utf-8

"""
    LEIA RESTful API for AI

    Leia API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: contact@leia.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Worker(object):
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
        'job_type': 'str',
        'number': 'int',
        'statuses': 'list[str]'
    }

    attribute_map = {
        'job_type': 'job_type',
        'number': 'number',
        'statuses': 'statuses'
    }

    def __init__(self, job_type=None, number=None, statuses=None):  # noqa: E501
        """Worker - a model defined in Swagger"""  # noqa: E501
        self._job_type = None
        self._number = None
        self._statuses = None
        self.discriminator = None
        self.job_type = job_type
        self.number = number
        self.statuses = statuses

    @property
    def job_type(self):
        """Gets the job_type of this Worker.  # noqa: E501


        :return: The job_type of this Worker.  # noqa: E501
        :rtype: str
        """
        return self._job_type

    @job_type.setter
    def job_type(self, job_type):
        """Sets the job_type of this Worker.


        :param job_type: The job_type of this Worker.  # noqa: E501
        :type: str
        """
        if job_type is None:
            raise ValueError("Invalid value for `job_type`, must not be `None`")  # noqa: E501

        self._job_type = job_type

    @property
    def number(self):
        """Gets the number of this Worker.  # noqa: E501


        :return: The number of this Worker.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this Worker.


        :param number: The number of this Worker.  # noqa: E501
        :type: int
        """
        if number is None:
            raise ValueError("Invalid value for `number`, must not be `None`")  # noqa: E501

        self._number = number

    @property
    def statuses(self):
        """Gets the statuses of this Worker.  # noqa: E501


        :return: The statuses of this Worker.  # noqa: E501
        :rtype: list[str]
        """
        return self._statuses

    @statuses.setter
    def statuses(self, statuses):
        """Sets the statuses of this Worker.


        :param statuses: The statuses of this Worker.  # noqa: E501
        :type: list[str]
        """
        if statuses is None:
            raise ValueError("Invalid value for `statuses`, must not be `None`")  # noqa: E501

        self._statuses = statuses

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
        if issubclass(Worker, dict):
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
        if not isinstance(other, Worker):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
