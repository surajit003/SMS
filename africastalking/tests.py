from django.test import TestCase
from .utils import send_sms_request
from mock import patch, Mock
from message.models import Gateway
from django.conf import settings
import requests


class SMSTaskTests(TestCase):

    def setUp(self):
        self.gateway = Gateway.objects.create(name='Africastalking', active=True,
                                              api_url='https://api.sandbox.africastalking.com/version1/messaging',
                                              password=settings.AT_PASSWORD,
                                              configured_sender=settings.AT_USERNAME,
                                              account_number=settings.AT_USERNAME
                                              )

    def test_send_sms_request(self):
        with patch.object(requests, 'post') as mock_obj:
            fake_response = {'hello': 'world'}
            mock_obj.return_value = mock_response = Mock()
            mock_response.content = fake_response
            test_headers = {}
            actual_response = send_sms_request('', test_headers, '')
            self.assertEqual(actual_response, fake_response)
