import json
import unittest

import mock
import requests

import websms

OK_RESPONSE = json.dumps(
    {
        'statusCode': 2000,
        'statusMessage': 'OK',
        'clientMessageId': None,
        'transferId': '006214b5440071843da1',
        'smsCount': 1,
    }
)

NOT_OK_RESPONSE = json.dumps(
    {
        'statusCode': 4003,
        'statusMessage': 'sender address or type is invalid',
        'clientMessageId': None,
        'transferId': None,
        'smsCount': 0,
    }
)

INVALID_RESPONSE = json.dumps({'message': 'Lorem Ipsum Dolor Sit amet'})


class SMSSendResponseTestCase(unittest.TestCase):
    """Tests for `SMSSendResponse` class"""

    def test_repr_ok(self):
        """Test object representation. OK response."""
        response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(repr(response), '<SMSSendResponse [2000]>')

    def test_status_code_ok(self):
        """Test `status_code` property. OK response."""
        response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(response.status_code, 2000)

    def test_status_message_ok(self):
        """Test `status_message` property. OK response."""
        response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(response.status_message, 'OK')

    def test_transfer_id_ok(self):
        """Test `transfer_id` property. OK response."""
        response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(response.transfer_id, '006214b5440071843da1')

    def test_sms_count_ok(self):
        """Test `sms_count` property. OK response."""
        response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(response.sms_count, 1)

    def test_repr_not_ok(self):
        """Test object representation. Not OK response."""
        response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertEqual(repr(response), '<SMSSendResponse [4003]>')

    def test_status_code_not_ok(self):
        """Test `status_code` property. Not OK response."""
        response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertEqual(response.status_code, 4003)

    def test_status_message_not_ok(self):
        """Test `status_message` property. Not OK response."""
        response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertEqual(
            response.status_message, 'sender address or type is invalid'
        )

    def test_transfer_id_not_ok(self):
        """Test `transfer_id` property. Not OK response."""
        response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertIsNone(response.transfer_id)

    def test_sms_count_not_ok(self):
        """Test `sms_count` property. Not OK response."""
        response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertEqual(response.sms_count, 0)

    def test_repr_invalid(self):
        """Test object representation. Invalid response."""
        response = websms.SMSSendResponse(INVALID_RESPONSE)
        self.assertEqual(repr(response), '<SMSSendResponse []>')

    def test_status_code_invalid(self):
        """Test `status_code` property. Invalid response."""
        response = websms.SMSSendResponse(INVALID_RESPONSE)
        self.assertIsNone(response.status_code)

    def test_status_message_invalid(self):
        """Test `status_message` property. Invalid response."""
        response = websms.SMSSendResponse(INVALID_RESPONSE)
        self.assertIsNone(response.status_message)

    def test_transfer_id_invalid(self):
        """Test `transfer_id` property. Invalid response."""
        response = websms.SMSSendResponse(INVALID_RESPONSE)
        self.assertIsNone(response.transfer_id)

    def test_sms_count_invalid(self):
        """Test `sms_count` property. Invalid response."""
        response = websms.SMSSendResponse(INVALID_RESPONSE)
        self.assertIsNone(response.sms_count)


class SMSServiceTestCase(unittest.TestCase):
    """Tests for `SMSService` class"""

    def test_repr(self):
        """Test object representation."""
        service = websms.SMSService(username='user', password='pass')

        self.assertEqual(repr(service), '<SMSService user>')

    def test_default_service_attributes(self):
        """Test class default attributes."""
        self.assertEqual(
            websms.default_service.api_url, websms.SMSService.SMS_API_URL
        )
        self.assertIsNone(websms.default_service.username)
        self.assertIsNone(websms.default_service.password)
        self.assertIsNone(websms.default_service.sender_address)
        self.assertIsNone(websms.default_service.sender_address_type)
        self.assertIsNone(websms.default_service.max_sms_per_message)
        self.assertIsNone(websms.default_service.timeout)

    def test_init_default_attributes(self):
        """Test class default attributes initialization."""
        service = websms.SMSService()

        self.assertEqual(service.api_url, websms.default_service.api_url)
        self.assertEqual(service.username, websms.default_service.username)
        self.assertEqual(service.password, websms.default_service.password)
        self.assertEqual(
            service.sender_address, websms.default_service.sender_address
        )
        self.assertEqual(
            service.sender_address_type,
            websms.default_service.sender_address_type,
        )
        self.assertEqual(
            service.max_sms_per_message,
            websms.default_service.max_sms_per_message,
        )
        self.assertEqual(service.timeout, websms.default_service.timeout)

    def test_init_custom_attributes(self):
        """Test class custom attributes initialization."""
        custom_api_url = 'http://localhost:8000/post.php'
        custom_username = 'johndoe'
        custom_password = 'admin.1'
        custom_sender_address = 'Foo'
        custom_sender_address_type = 'alphanumeric'
        custom_max_sms_per_message = 3
        custom_timeout = 30

        service = websms.SMSService(
            api_url=custom_api_url,
            username=custom_username,
            password=custom_password,
            sender_address=custom_sender_address,
            sender_address_type=custom_sender_address_type,
            max_sms_per_message=custom_max_sms_per_message,
            timeout=custom_timeout,
        )

        self.assertEqual(service.api_url, custom_api_url)
        self.assertEqual(service.username, custom_username)
        self.assertEqual(service.password, custom_password)
        self.assertEqual(service.sender_address, custom_sender_address)
        self.assertEqual(
            service.sender_address_type, custom_sender_address_type
        )
        self.assertEqual(
            service.max_sms_per_message, custom_max_sms_per_message
        )
        self.assertEqual(service.timeout, custom_timeout)

    def test_configure(self):
        """Test for `configure()` method."""
        custom_api_url = 'http://localhost:8000/post.php'
        custom_username = 'johndoe'
        custom_password = 'admin.1'
        custom_sender_address = 'Foo'
        custom_sender_address_type = 'alphanumeric'
        custom_max_sms_per_message = 3
        custom_timeout = 30

        service = websms.SMSService()
        service.configure(
            api_url=custom_api_url,
            username=custom_username,
            password=custom_password,
            sender_address=custom_sender_address,
            sender_address_type=custom_sender_address_type,
            max_sms_per_message=custom_max_sms_per_message,
            timeout=custom_timeout,
        )

        self.assertEqual(service.api_url, custom_api_url)
        self.assertEqual(service.username, custom_username)
        self.assertEqual(service.password, custom_password)
        self.assertEqual(service.sender_address, custom_sender_address)
        self.assertEqual(
            service.sender_address_type, custom_sender_address_type
        )
        self.assertEqual(
            service.max_sms_per_message, custom_max_sms_per_message
        )
        self.assertEqual(service.timeout, custom_timeout)

    @mock.patch('websms.requests.post')
    def test_post_sms_ok_default_params(self, mock_post):
        """Test `post_sms()` method, OK, default params."""
        type(mock_post.return_value).text = mock.PropertyMock(
            return_value=OK_RESPONSE
        )
        service = websms.SMSService(username='user', password='pass')

        response = service.post_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': False,
            },
            auth=('user', 'pass'),
            timeout=None,
        )
        self.assertIsInstance(response, websms.SMSSendResponse)
        self.assertEqual(response.status_code, 2000)
        self.assertEqual(response.status_message, 'OK')
        self.assertEqual(response.transfer_id, '006214b5440071843da1')
        self.assertEqual(response.sms_count, 1)

    @mock.patch('websms.requests.post')
    def test_post_sms_ok_custom_params(self, mock_post):
        """Test `post_sms()` method, OK, custom params."""
        type(mock_post.return_value).text = mock.PropertyMock(
            return_value=OK_RESPONSE
        )
        service = websms.SMSService(username='user', password='pass')

        response = service.post_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            max_sms_per_message=5,
            test=True,
            timeout=30,
            sender_address='Foo',
            sender_address_type='alphanumeric',
        )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': True,
                'senderAddress': 'Foo',
                'senderAddressType': 'alphanumeric',
                'maxSmsPerMessage': '5',
            },
            auth=('user', 'pass'),
            timeout=30,
        )
        self.assertIsInstance(response, websms.SMSSendResponse)
        self.assertEqual(response.status_code, 2000)
        self.assertEqual(response.status_message, 'OK')
        self.assertEqual(response.transfer_id, '006214b5440071843da1')
        self.assertEqual(response.sms_count, 1)

    @mock.patch('websms.requests.post')
    def test_post_sms_error_missing_credentials(self, mock_post):
        """Test `post_sms()` method, ERROR, missing credentials."""
        service = websms.SMSService()

        with self.assertRaises(websms.ConfigurationError):
            service.post_sms(
                recipients_address_list=['+4911122233344'],
                message_content='Hello!',
            )

        mock_post.assert_not_called()

    @mock.patch('websms.requests.post')
    def test_post_sms_error_response(self, mock_post):
        """Test `post_sms()` method, ERROR, RequestError."""
        type(mock_post.return_value).text = mock.PropertyMock(
            return_value=NOT_OK_RESPONSE
        )
        service = websms.SMSService(username='user', password='pass')

        with self.assertRaises(websms.RequestError) as raised:
            service.post_sms(
                recipients_address_list=['+4911122233344'],
                message_content='Hello!',
            )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': False,
            },
            auth=('user', 'pass'),
            timeout=None,
        )
        self.assertEqual(
            str(raised.exception), 'sender address or type is invalid'
        )

    @mock.patch('websms.requests.post', side_effect=requests.ConnectTimeout)
    def test_post_sms_error_network(self, mock_post):
        """Test `post_sms()` method, ERROR, CommunicationError."""
        service = websms.SMSService(username='user', password='pass')

        with self.assertRaises(websms.CommunicationError) as raised:
            service.post_sms(
                recipients_address_list=['+4911122233344'],
                message_content='Hello!',
            )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': False,
            },
            auth=('user', 'pass'),
            timeout=None,
        )
        self.assertIsInstance(
            raised.exception.original_exception, requests.ConnectTimeout
        )

    @mock.patch('websms.requests.post')
    def test_post_sms_error_http(self, mock_post):
        """Test `post_sms()` method, ERROR, HTTPError."""
        type(mock_post.return_value).text = mock.PropertyMock(
            return_value='Something is wrong'
        )
        type(mock_post.return_value).raise_for_status = mock.MagicMock(
            side_effect=requests.HTTPError
        )
        service = websms.SMSService(username='user', password='pass')

        with self.assertRaises(websms.RequestError) as raised:
            service.post_sms(
                recipients_address_list=['+4911122233344'],
                message_content='Hello!',
            )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': False,
            },
            auth=('user', 'pass'),
            timeout=None,
        )
        self.assertIsInstance(
            raised.exception.original_exception, requests.HTTPError
        )

    @mock.patch('websms.requests.post', side_effect=requests.ConnectTimeout)
    def test_post_sms_error_fail_silently(self, mock_post):
        """Test `post_sms()` method, ERROR, ConnectTimeout, fail_silently."""
        type(mock_post.return_value).text = mock.PropertyMock(
            return_value='REQUEST ERROR\nerror = Something is wrong'
        )
        service = websms.SMSService(username='user', password='pass')

        response = service.post_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            fail_silently=True,
        )

        mock_post.assert_called_once_with(
            url=websms.SMSService.SMS_API_URL,
            json={
                'recipientAddressList': ['+4911122233344'],
                'messageContent': 'Hello!',
                'test': False,
            },
            auth=('user', 'pass'),
            timeout=None,
        )
        self.assertIsNone(response)

    @mock.patch(
        'websms.SMSService.post_sms',
        return_value=websms.SMSSendResponse(OK_RESPONSE),
    )
    def test_send_ok_default_params(self, mock_post_sms):
        """Test `send()` method, OK, default params."""
        service = websms.SMSService()
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )
        transfer_id = service.send(sms)

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address=None,
            sender_address_type=None,
            test=False,
            max_sms_per_message=None,
            timeout=None,
            fail_silently=False,
        )
        self.assertEqual(transfer_id, '006214b5440071843da1')
        self.assertIsInstance(sms.post_response, websms.SMSSendResponse)

    @mock.patch(
        'websms.SMSService.post_sms',
        return_value=websms.SMSSendResponse(OK_RESPONSE),
    )
    def test_send_ok_custom_params(self, mock_post_sms):
        """Test `send()` method, OK, custom params."""
        service = websms.SMSService()
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            max_sms_per_message=5,
            test=True,
            sender_address='Foo',
            sender_address_type='alphanumeric',
        )

        transfer_id = service.send(sms, timeout=30, fail_silently=True)

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address='Foo',
            sender_address_type='alphanumeric',
            test=True,
            max_sms_per_message=5,
            timeout=30,
            fail_silently=True,
        )
        self.assertEqual(transfer_id, '006214b5440071843da1')
        self.assertIsInstance(sms.post_response, websms.SMSSendResponse)

    @mock.patch(
        'websms.SMSService.post_sms',
        side_effect=websms.RequestError('Error occurred'),
    )
    def test_send_service_error(self, mock_post_sms):
        """Test `send()` method, ERROR."""
        service = websms.SMSService()
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        with self.assertRaises(websms.RequestError):
            service.send(sms)

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address=None,
            sender_address_type=None,
            test=False,
            max_sms_per_message=None,
            timeout=None,
            fail_silently=False,
        )
        self.assertIsNone(sms.post_response)


class SMSTestCase(unittest.TestCase):
    """Tests for `SMS` class"""

    def test_init_default_attributes(self):
        """Test class default attributes initialization."""
        recipients_address_list = ['+4911122233344']
        message_content = 'Hello!'

        sms = websms.SMS(
            recipients_address_list=recipients_address_list,
            message_content=message_content,
        )

        self.assertEqual(sms.recipients_address_list, recipients_address_list)
        self.assertEqual(sms.message_content, message_content)
        self.assertIsNone(sms.sender_address)
        self.assertIsNone(sms.sender_address_type)
        self.assertFalse(sms.test)
        self.assertIsNone(sms.transfer_id)
        self.assertIsNone(sms.max_sms_per_message)

    def test_init_custom_attributes(self):
        """Test class custom attributes initialization."""
        recipients_address_list = ['+4911122233344']
        message_content = 'Hello!'
        custom_sender_address = 'Foo'
        custom_sender_address_type = 'alphanumeric'
        custom_test = True
        custom_max_sms_per_message = 5

        sms = websms.SMS(
            recipients_address_list=recipients_address_list,
            message_content=message_content,
            sender_address=custom_sender_address,
            sender_address_type=custom_sender_address_type,
            test=custom_test,
            max_sms_per_message=custom_max_sms_per_message,
        )

        self.assertEqual(sms.recipients_address_list, recipients_address_list)
        self.assertEqual(sms.message_content, message_content)
        self.assertEqual(sms.sender_address, custom_sender_address)
        self.assertEqual(sms.sender_address_type, custom_sender_address_type)
        self.assertEqual(sms.test, custom_test)
        self.assertEqual(sms.max_sms_per_message, custom_max_sms_per_message)

    def test_repr(self):
        """Test object representation."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )
        self.assertEqual(repr(sms), "<SMS ['+4911122233344']>")

        sms.post_response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(
            repr(sms), "<SMS ['+4911122233344'] [006214b5440071843da1]>"
        )

    @mock.patch('websms.SMSService.send')
    def test_send_default_parameters(self, mock_send):
        """Test `send()` method, OK, default params."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        sms.send()

        mock_send.assert_called_once_with(
            sms, timeout=None, fail_silently=False
        )

    @mock.patch('websms.SMSService.send')
    def test_send_custom_parameters(self, mock_send):
        """Test `send()` method, OK, custom params."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        sms.send(timeout=30, fail_silently=True)

        mock_send.assert_called_once_with(sms, timeout=30, fail_silently=True)

    @mock.patch('websms.SMSService.send')
    def test_send_custom_service(self, mock_send):
        """Test `send()` method, OK, custom service."""
        mock_service = mock.MagicMock()
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        sms.send(service=mock_service)

        mock_service.send.assert_called_once_with(
            sms, timeout=None, fail_silently=False
        )
        mock_send.assert_not_called()

    def test_transfer_id_no_post_response(self):
        """Test `transfer_id` is `None`, no POST response."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )
        self.assertIsNone(sms.transfer_id)

    def test_transfer_id_with_post_ok_response(self):
        """Test `transfer_id` is not `None`, POST OK response."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )
        sms.post_response = websms.SMSSendResponse(OK_RESPONSE)
        self.assertEqual(sms.transfer_id, '006214b5440071843da1')

    def test_transfer_id_with_post_response(self):
        """Test `transfer_id` is `None`, POST Not OK response."""
        sms = websms.SMS(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )
        sms.post_response = websms.SMSSendResponse(NOT_OK_RESPONSE)
        self.assertIsNone(sms.transfer_id)


class FunctionsTestCase(unittest.TestCase):
    """Tests for top-level functions: `send_sms`, `configure`."""

    @mock.patch(
        'websms.SMSService.post_sms',
        return_value=websms.SMSSendResponse(OK_RESPONSE),
    )
    def test_send_sms_ok_default_params(self, mock_post_sms):
        """Test `send_sms()` function, OK, default params."""
        transfer_id = websms.send_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address=None,
            sender_address_type=None,
            test=False,
            max_sms_per_message=None,
            timeout=None,
            fail_silently=False,
        )
        self.assertEqual(transfer_id, '006214b5440071843da1')

    @mock.patch(
        'websms.SMSService.post_sms',
        return_value=websms.SMSSendResponse(NOT_OK_RESPONSE),
    )
    def test_send_sms_not_ok_default_params(self, mock_post_sms):
        """Test `send_sms()` function, Not OK, default params."""
        transfer_id = websms.send_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
        )

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address=None,
            sender_address_type=None,
            test=False,
            max_sms_per_message=None,
            timeout=None,
            fail_silently=False,
        )
        self.assertIsNone(transfer_id)

    @mock.patch(
        'websms.SMSService.post_sms',
        return_value=websms.SMSSendResponse(OK_RESPONSE),
    )
    def test_send_sms_custom_params(self, mock_post_sms):
        """Test `send_sms()` function, custom params."""
        transfer_id = websms.send_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            max_sms_per_message=5,
            test=True,
            sender_address='Foo',
            sender_address_type='alphanumeric',
            timeout=30,
            fail_silently=True,
        )

        mock_post_sms.assert_called_once_with(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            sender_address='Foo',
            sender_address_type='alphanumeric',
            test=True,
            max_sms_per_message=5,
            timeout=30,
            fail_silently=True,
        )
        self.assertEqual(transfer_id, '006214b5440071843da1')

    def test_send_sms_custom_service(self):
        """Test `send_sms()` function, custom service."""
        mock_service = mock.MagicMock()
        websms.send_sms(
            recipients_address_list=['+4911122233344'],
            message_content='Hello!',
            service=mock_service,
        )
        mock_service.send.assert_called_once()

    @mock.patch('websms.default_service.configure')
    def test_configure(self, mock_configure):
        """Test `configure()` function."""
        custom_api_url = 'http://localhost:8000/post.php'
        custom_username = 'johndoe'
        custom_password = 'admin.1'
        custom_sender_address = 'Foo'
        custom_sender_address_type = 'alphanumeric'
        custom_max_sms_per_message = 3
        custom_timeout = 30

        websms.configure(
            api_url=custom_api_url,
            username=custom_username,
            password=custom_password,
            sender_address=custom_sender_address,
            sender_address_type=custom_sender_address_type,
            max_sms_per_message=custom_max_sms_per_message,
            timeout=custom_timeout,
        )
        mock_configure.assert_called_with(
            api_url=custom_api_url,
            username=custom_username,
            password=custom_password,
            sender_address=custom_sender_address,
            sender_address_type=custom_sender_address_type,
            max_sms_per_message=custom_max_sms_per_message,
            timeout=custom_timeout,
        )
