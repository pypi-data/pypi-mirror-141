# coding: utf-8

"""
    FINBOURNE Notifications API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.1.227
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid_notifications.configuration import Configuration


class UpdateWebhookNotification(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'description': 'str',
        'http_method': 'str',
        'url': 'str',
        'authentication_type': 'str',
        'authentication_configuration_item_paths': 'dict(str, str)',
        'content_type': 'str',
        'content': 'object'
    }

    attribute_map = {
        'description': 'description',
        'http_method': 'httpMethod',
        'url': 'url',
        'authentication_type': 'authenticationType',
        'authentication_configuration_item_paths': 'authenticationConfigurationItemPaths',
        'content_type': 'contentType',
        'content': 'content'
    }

    required_map = {
        'description': 'required',
        'http_method': 'required',
        'url': 'required',
        'authentication_type': 'required',
        'authentication_configuration_item_paths': 'optional',
        'content_type': 'optional',
        'content': 'optional'
    }

    def __init__(self, description=None, http_method=None, url=None, authentication_type=None, authentication_configuration_item_paths=None, content_type=None, content=None, local_vars_configuration=None):  # noqa: E501
        """UpdateWebhookNotification - a model defined in OpenAPI"
        
        :param description:  The summary of the services provided by the notification (required)
        :type description: str
        :param http_method:  The HTTP method such as GET, POST, etc. to use on the request (required)
        :type http_method: str
        :param url:  The URL to send the request to (required)
        :type url: str
        :param authentication_type:  The type of authentication to use on the request (required)
        :type authentication_type: str
        :param authentication_configuration_item_paths:  The paths of the Configuration Store configuration items that contain the authentication configuration. Each  authentication type requires different keys:  - Lusid - None required  - BasicAuth - Requires 'Username' and 'Password'  - BearerToken - Requires 'BearerToken'                e.g. the following would be valid assuming that the config is present in the configuration store at the  specified paths:                    \"authenticationType\": \"BasicAuth\",      \"authenticationConfigurationItemPaths\": {          \"Username\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminUser\",          \"Password\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminPassword\"      }
        :type authentication_configuration_item_paths: dict(str, str)
        :param content_type:  The type of the content e.g. Json
        :type content_type: str
        :param content:  The content of the request
        :type content: object

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._http_method = None
        self._url = None
        self._authentication_type = None
        self._authentication_configuration_item_paths = None
        self._content_type = None
        self._content = None
        self.discriminator = None

        self.description = description
        self.http_method = http_method
        self.url = url
        self.authentication_type = authentication_type
        self.authentication_configuration_item_paths = authentication_configuration_item_paths
        self.content_type = content_type
        self.content = content

    @property
    def description(self):
        """Gets the description of this UpdateWebhookNotification.  # noqa: E501

        The summary of the services provided by the notification  # noqa: E501

        :return: The description of this UpdateWebhookNotification.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateWebhookNotification.

        The summary of the services provided by the notification  # noqa: E501

        :param description: The description of this UpdateWebhookNotification.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 512):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not re.search(r'^[\s\S]*$', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._description = description

    @property
    def http_method(self):
        """Gets the http_method of this UpdateWebhookNotification.  # noqa: E501

        The HTTP method such as GET, POST, etc. to use on the request  # noqa: E501

        :return: The http_method of this UpdateWebhookNotification.  # noqa: E501
        :rtype: str
        """
        return self._http_method

    @http_method.setter
    def http_method(self, http_method):
        """Sets the http_method of this UpdateWebhookNotification.

        The HTTP method such as GET, POST, etc. to use on the request  # noqa: E501

        :param http_method: The http_method of this UpdateWebhookNotification.  # noqa: E501
        :type http_method: str
        """
        if self.local_vars_configuration.client_side_validation and http_method is None:  # noqa: E501
            raise ValueError("Invalid value for `http_method`, must not be `None`")  # noqa: E501

        self._http_method = http_method

    @property
    def url(self):
        """Gets the url of this UpdateWebhookNotification.  # noqa: E501

        The URL to send the request to  # noqa: E501

        :return: The url of this UpdateWebhookNotification.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this UpdateWebhookNotification.

        The URL to send the request to  # noqa: E501

        :param url: The url of this UpdateWebhookNotification.  # noqa: E501
        :type url: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                url is not None and len(url) > 16384):
            raise ValueError("Invalid value for `url`, length must be less than or equal to `16384`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                url is not None and len(url) < 1):
            raise ValueError("Invalid value for `url`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                url is not None and not re.search(r'^([A-Za-z0-9-._~:\/?#[\]@!$&\'()*+,;%=]|(\{\{([a-zA-Z0-9\s])*\}\}))*$', url)):  # noqa: E501
            raise ValueError(r"Invalid value for `url`, must be a follow pattern or equal to `/^([A-Za-z0-9-._~:\/?#[\]@!$&'()*+,;%=]|(\{\{([a-zA-Z0-9\s])*\}\}))*$/`")  # noqa: E501

        self._url = url

    @property
    def authentication_type(self):
        """Gets the authentication_type of this UpdateWebhookNotification.  # noqa: E501

        The type of authentication to use on the request  # noqa: E501

        :return: The authentication_type of this UpdateWebhookNotification.  # noqa: E501
        :rtype: str
        """
        return self._authentication_type

    @authentication_type.setter
    def authentication_type(self, authentication_type):
        """Sets the authentication_type of this UpdateWebhookNotification.

        The type of authentication to use on the request  # noqa: E501

        :param authentication_type: The authentication_type of this UpdateWebhookNotification.  # noqa: E501
        :type authentication_type: str
        """
        if self.local_vars_configuration.client_side_validation and authentication_type is None:  # noqa: E501
            raise ValueError("Invalid value for `authentication_type`, must not be `None`")  # noqa: E501

        self._authentication_type = authentication_type

    @property
    def authentication_configuration_item_paths(self):
        """Gets the authentication_configuration_item_paths of this UpdateWebhookNotification.  # noqa: E501

        The paths of the Configuration Store configuration items that contain the authentication configuration. Each  authentication type requires different keys:  - Lusid - None required  - BasicAuth - Requires 'Username' and 'Password'  - BearerToken - Requires 'BearerToken'                e.g. the following would be valid assuming that the config is present in the configuration store at the  specified paths:                    \"authenticationType\": \"BasicAuth\",      \"authenticationConfigurationItemPaths\": {          \"Username\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminUser\",          \"Password\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminPassword\"      }  # noqa: E501

        :return: The authentication_configuration_item_paths of this UpdateWebhookNotification.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._authentication_configuration_item_paths

    @authentication_configuration_item_paths.setter
    def authentication_configuration_item_paths(self, authentication_configuration_item_paths):
        """Sets the authentication_configuration_item_paths of this UpdateWebhookNotification.

        The paths of the Configuration Store configuration items that contain the authentication configuration. Each  authentication type requires different keys:  - Lusid - None required  - BasicAuth - Requires 'Username' and 'Password'  - BearerToken - Requires 'BearerToken'                e.g. the following would be valid assuming that the config is present in the configuration store at the  specified paths:                    \"authenticationType\": \"BasicAuth\",      \"authenticationConfigurationItemPaths\": {          \"Username\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminUser\",          \"Password\": \"config://personal/myUserId/WebhookConfigurations/ExampleService/AdminPassword\"      }  # noqa: E501

        :param authentication_configuration_item_paths: The authentication_configuration_item_paths of this UpdateWebhookNotification.  # noqa: E501
        :type authentication_configuration_item_paths: dict(str, str)
        """

        self._authentication_configuration_item_paths = authentication_configuration_item_paths

    @property
    def content_type(self):
        """Gets the content_type of this UpdateWebhookNotification.  # noqa: E501

        The type of the content e.g. Json  # noqa: E501

        :return: The content_type of this UpdateWebhookNotification.  # noqa: E501
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """Sets the content_type of this UpdateWebhookNotification.

        The type of the content e.g. Json  # noqa: E501

        :param content_type: The content_type of this UpdateWebhookNotification.  # noqa: E501
        :type content_type: str
        """

        self._content_type = content_type

    @property
    def content(self):
        """Gets the content of this UpdateWebhookNotification.  # noqa: E501

        The content of the request  # noqa: E501

        :return: The content of this UpdateWebhookNotification.  # noqa: E501
        :rtype: object
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this UpdateWebhookNotification.

        The content of the request  # noqa: E501

        :param content: The content of this UpdateWebhookNotification.  # noqa: E501
        :type content: object
        """

        self._content = content

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateWebhookNotification):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateWebhookNotification):
            return True

        return self.to_dict() != other.to_dict()
