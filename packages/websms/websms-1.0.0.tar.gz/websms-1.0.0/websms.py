import json
import logging
from typing import List, Optional, Tuple, Union

import requests

logger = logging.getLogger('websms')


class SMSServiceError(Exception):
    """Base exception class."""

    def __init__(
        self,
        message: Optional[str] = None,
        original_exception: Optional[requests.RequestException] = None,
    ):
        message = message or str(original_exception)
        super().__init__(message)
        self.original_exception = original_exception

    def is_timeout(self):
        """Is this error caused by timeout?"""
        return self.original_exception and isinstance(
            self.original_exception, requests.Timeout
        )


class ConfigurationError(SMSServiceError):
    """Service is improperly configured."""


class CommunicationError(SMSServiceError):
    """Unable to communicate to API."""


class RequestError(SMSServiceError):
    """API responded with an error."""


class SMSSendResponse(object):
    """Wrapper over SMSService response data, providing dict-like access."""

    def __init__(self, response_text: str) -> None:
        self._data = json.loads(response_text)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} [{self.status_code or ""}]>'

    def __getitem__(self, item) -> Union[str, int]:
        return self._data[item]

    def get(self, key, default=None) -> Optional[Union[str, int]]:
        """Retrieve a value of a given key from a parsed JSON data."""
        try:
            value = self[key]
        except KeyError:
            value = default
        return value

    @property
    def status_code(self):
        """Current status code of sent SMS."""
        return self.get('statusCode')

    @property
    def status_message(self):
        """Description of the response status code."""
        return self.get('statusMessage')

    @property
    def transfer_id(self):
        """Unique ID that is set after successful processing of the request."""
        return self.get('transferId')

    @property
    def sms_count(self):
        """Number of generated SMS."""
        return self.get('smsCount')


class SMSService(object):
    """Main object - provider's API client."""

    SMS_API_URL = 'https://api.websms.com/rest/smsmessaging/text'

    def __init__(
        self,
        api_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sender_address: Optional[str] = None,
        sender_address_type: Optional[str] = None,
        max_sms_per_message: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        """Initializes SMSService object.

        :param api_url: SMS sending webservice URL
        :param username: username for access to websms platform - REQUIRED
        :param password: password for access to websms platform - REQUIRED
        :param sender_address: address of the sender from which the message
            is sent (optional)
        :param sender_address_type: SMS sender format, possible options:
            national, international, alphanumeric, shortcode (optional)
        :param max_sms_per_message: The maximum number of discrete SMS,
            to which a long text-SMS will be split
            (optional, implicit default - 1)
        :param timeout: network timeout in seconds (optional)
        """
        self.api_url = api_url or self.SMS_API_URL
        self.username = username
        self.password = password
        self.sender_address = sender_address
        self.sender_address_type = sender_address_type
        self.max_sms_per_message = max_sms_per_message
        self.timeout = timeout

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.username}>'

    def configure(self, **kwargs):
        """Allows change SMSService parameters set in constructor.

        Available options:
        `api_url`: SMS sending webservice URL
        `username`: username for access to websms platform - REQUIRED
        `password`: password for access to websms platform - REQUIRED
        `sender_address`: SMS sender address or name (optional)
        `sender_address_type`: SMS sender format, possible options:
            national, international, alphanumeric, shortcode  (optional)
        `max_sms_per_message`: The maximum number of discrete SMS, to which
            a long text-SMS will be split (optional, implicit default - 1)
        `timeout`: network timeout in seconds (optional)
        """
        for name, value in kwargs.items():
            setattr(self, name, value)

    # High-level API:

    def send(
        self,
        sms: 'SMS',
        timeout: Optional[float] = None,
        fail_silently: bool = False,
    ) -> Optional[str]:
        """Sends SMS via websms platform by calling `post_sms`.
        Populates `SMS.post_response` attribute.

        :param sms: an SMS instance
        :param timeout: network timeout in seconds
        :param fail_silently: do not raise exceptions

        :raise ConfigurationError: client is improperly configured
        :raise RequestError: remote API responded with error message or
            HTTP error status
        :raise CommunicationError: unable to communicate with remote API

        :return: `transfer_id` if SMS is sent, `None` otherwise
        """
        try:
            post_response = self.post_sms(
                recipients_address_list=sms.recipients_address_list,
                message_content=sms.message_content,
                sender_address=sms.sender_address,
                sender_address_type=sms.sender_address_type,
                test=sms.test,
                max_sms_per_message=sms.max_sms_per_message,
                timeout=timeout,
                fail_silently=fail_silently,
            )
        except Exception:
            sms.post_response = None
            raise
        else:
            sms.post_response = post_response

        return post_response.transfer_id if post_response else None

    # Low-level API:

    def post_sms(
        self,
        recipients_address_list: List[str],
        message_content: str,
        sender_address: Optional[str] = None,
        sender_address_type: Optional[str] = None,
        test: bool = False,
        max_sms_per_message: Optional[int] = None,
        timeout: Optional[float] = None,
        fail_silently: bool = False,
    ) -> Optional[SMSSendResponse]:
        """Sends SMS via websms platform.

        :param recipients_address_list: list of recipient's phone numbers
        :param message_content: message to be sent
        :param sender_address: address of the sender from which the message
            is sent (optional)
        :param sender_address_type: SMS sender format, possible options:
            national, international, alphanumeric, shortcode (optional)
        :param test: simulate SMS sending
        :param max_sms_per_message: The maximum number of discrete SMS,
            to which a long text-SMS will be split
            (optional, implicit default - 1)
        :param timeout: network timeout in seconds
        :param fail_silently: do not raise exceptions

        :raise ConfigurationError: client is improperly configured
        :raise RequestError: remote API responded with error message or
            HTTP error status
        :raise CommunicationError: unable to communicate with remote API

        :return: `SMSSendResponse` object or `None`
        """
        if not (self.username and self.password):
            raise ConfigurationError('Service credentials not defined')

        auth = (self.username, self.password)

        data = {
            'recipientAddressList': recipients_address_list,
            'messageContent': message_content,
            'test': test,
        }

        sender_address = sender_address or self.sender_address
        if sender_address:
            data['senderAddress'] = sender_address

        sender_address_type = sender_address_type or self.sender_address_type
        if sender_address_type:
            data['senderAddressType'] = sender_address_type

        max_sms_per_message = max_sms_per_message or self.max_sms_per_message
        if max_sms_per_message:
            data['maxSmsPerMessage'] = str(max_sms_per_message)

        if timeout is None:
            timeout = self.timeout

        return self._request(
            url=self.api_url,
            data=data,
            auth=auth,
            timeout=timeout,
            resource_name='Post SMS',
            fail_silently=fail_silently,
        )

    @staticmethod
    def _request(
        url: str,
        data: dict,
        auth: Tuple[Optional[str], Optional[str]],
        timeout: float,
        resource_name: str,
        fail_silently: bool,
    ) -> Optional[SMSSendResponse]:
        """Send a request to Service API, construct SMSSendResponse object from
        the response.

        :param url: destination's URL address
        :param data: POST data
        :param auth: HTTP Basic Auth data
        :param timeout: network timeout in seconds
        :param resource_name: destination's verbose name (for logging)
        :param fail_silently: do not raise exceptions

        :raise RequestError: remote API responded with error message or
            HTTP error status
        :raise CommunicationError: unable to communicate with remote API

        :return: `SMSSendResponse` object or `None`
        """
        try:
            response = requests.post(
                url=url, json=data, auth=auth, timeout=timeout
            )
            logger.debug(
                '{} response: {} {}'.format(
                    resource_name, response.status_code, response.reason
                )
            )
            response.raise_for_status()
        except requests.RequestException as error:
            if isinstance(error, requests.HTTPError):
                exception_class = RequestError
            else:
                exception_class = CommunicationError
            exception = exception_class(original_exception=error)
            logger.error(exception)

            sms_response = None
            if not fail_silently:
                raise exception
        else:
            sms_response = SMSSendResponse(response.text)
            if not sms_response.transfer_id:
                exception = RequestError(sms_response.status_message)
                logger.error(exception)

                sms_response = None
                if not fail_silently:
                    raise exception

        return sms_response


default_service = SMSService()


class SMS(object):
    """Single message wrapper."""

    def __init__(
        self,
        recipients_address_list: List[str],
        message_content: str,
        sender_address: Optional[str] = None,
        sender_address_type: Optional[str] = None,
        test: bool = False,
        max_sms_per_message: Optional[int] = None,
    ):
        """Initializes SMS object - a single message.

        :param recipients_address_list: list of recipient's phone numbers
        :param message_content: message to be sent
        :param sender_address: address of the sender from which the message
            is sent (optional)
        :param sender_address_type: SMS sender format, possible options:
            national, international, alphanumeric, shortcode (optional)
        :param test: simulate SMS sending
        :param max_sms_per_message: The maximum number of discrete SMS,
            to which a long text-SMS will be split
            (optional, implicit default - 1)
        """
        self.recipients_address_list = recipients_address_list
        self.message_content = message_content
        self.sender_address = sender_address
        self.sender_address_type = sender_address_type
        self.test = test
        self.max_sms_per_message = max_sms_per_message
        self.post_response = None

    def __repr__(self):
        transfer_id = f' [{self.transfer_id}]' if self.transfer_id else ''
        class_name = self.__class__.__name__
        return f'<{class_name} {self.recipients_address_list}{transfer_id}>'

    def send(
        self,
        timeout: Optional[float] = None,
        fail_silently: bool = False,
        service: Optional[SMSService] = None,
    ) -> Optional[str]:
        """Send this SMS.

        :param timeout: network timeout in seconds
        :param fail_silently: do not raise exceptions
        :param service: a SMSService instance

        :raise ConfigurationError: client is improperly configured
        :raise RequestError: remote API responded with error message or
            HTTP error status
        :raise CommunicationError: unable to communicate with remote API

        :return: `transfer_id` if SMS is sent, `None` otherwise
        """
        service = service or default_service
        return service.send(self, timeout=timeout, fail_silently=fail_silently)

    @property
    def transfer_id(self) -> Optional[str]:
        """SMS unique transfer ID."""
        return self.post_response.transfer_id if self.post_response else None


# Shortcut functions, bypassing OOP API:


def send_sms(
    recipients_address_list: List[str],
    message_content: str,
    sender_address: Optional[str] = None,
    sender_address_type: Optional[str] = None,
    test: bool = False,
    max_sms_per_message: Optional[int] = None,
    timeout: Optional[float] = None,
    fail_silently: bool = False,
    service: Optional[SMSService] = None,
) -> Optional[str]:
    """Shortcut to send the SMS.

    :param recipients_address_list: list of recipient's phone numbers
    :param message_content: message to be sent
    :param sender_address: address of the sender from which the message
            is sent (optional)
    :param sender_address_type: SMS sender format, possible options:
        national, international, alphanumeric, shortcode (optional)
    :param test: simulate SMS sending
    :param max_sms_per_message: The maximum number of discrete SMS, to which
        a long text-SMS will be split (optional, implicit default - 1)
    :param timeout: network timeout in seconds
    :param fail_silently: do not raise exceptions
    :param service: a SMSService instance

    :raise ConfigurationError: client is improperly configured
    :raise RequestError: remote API responded with error message or
        HTTP error status
    :raise CommunicationError: unable to communicate with remote API

    :return: `transfer_id` if SMS is sent, `None` otherwise
    """
    sms = SMS(
        recipients_address_list=recipients_address_list,
        message_content=message_content,
        sender_address=sender_address,
        sender_address_type=sender_address_type,
        test=test,
        max_sms_per_message=max_sms_per_message,
    )
    return sms.send(
        timeout=timeout, fail_silently=fail_silently, service=service
    )


def configure(**kwargs):
    """Configure default SMSService instance.

    Available options:
    `api_url`: SMS sending webservice URL
    `username`: username for access to websms platform - REQUIRED
    `password`: password for access to websms platform - REQUIRED
    `sender_address`: SMS sender address or name (optional)
    `sender_address_type`: SMS sender format, possible options:
            national, international, alphanumeric, shortcode  (optional)
    `max_sms_per_message`: The maximum number of discrete SMS, to which
        a long text-SMS will be split (optional, implicit default - 1)
    `timeout`: network timeout in seconds (optional)
    """
    default_service.configure(**kwargs)
