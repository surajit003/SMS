from django.test import TestCase
from .utils import send_sms_request, send_sms_via_at,validate_recipients
from mock import patch, Mock
from message.models import Gateway
from django.conf import settings
import requests
import json


class SMSTaskTests(TestCase):
    def setUp(self):
        self.gateway = Gateway.objects.create(
            name="Africastalking",
            active=True,
            api_url="https://api.sandbox.africastalking.com/version1/messaging",
            password=settings.AT_PASSWORD,
            configured_sender=settings.AT_USERNAME,
            account_number=settings.AT_USERNAME,
        )

    def test_send_sms_request(self):
        with patch.object(requests, "post") as mock_obj:
            mock_obj.return_value = mock_response = Mock()
            mock_response.status_code=201
            resp,status_code=send_sms_request('','','')
            self.assertEqual(resp,mock_response)
            self.assertEqual(status_code,201)

    def test_sms_via_at(self):
        recipient = ["+254728282828", "+25472383883"]
        with patch.object(requests, "post") as mock_obj:
            fake_response = json.dumps(
                {
                    "SMSMessageData": {
                        "Message": "Sent to 2/2 Total Cost: KES 1.6000",
                        "Recipients": [
                            {
                                "statusCode": 101,
                                "number": "+25472929298",
                                "cost": "KES 0.8000",
                                "status": "Success",
                                "messageId": "ATXid_89c12c24448c87f8bfe4548f935e0ec4",
                            },
                            {
                                "statusCode": 101,
                                "number": "+25472929292",
                                "cost": "KES 0.8000",
                                "status": "Success",
                                "messageId": "ATXid_d4814306596b9989f4b0d3b9002ad3e4",
                            },
                        ],
                    }
                }
            )
            mock_obj.return_value = mock_response = Mock()
            mock_response.content = fake_response
            mock_response.status_code = 201
            actual_response = send_sms_via_at(recipient, "hello world")
            self.assertEqual(actual_response, json.loads(fake_response))

    def test_validate_recipients_with_valid_phone_numbers(self):
        recipients = ['+254771621351','+254771621352']
        self.assertEqual(validate_recipients(recipients),recipients)

    def test_validate_recipients_with_validandinvalidphonenumbers(self):
        recipients = ['+828299292','+254771621352']
        self.assertEqual(validate_recipients(recipients),['+254771621352'])




