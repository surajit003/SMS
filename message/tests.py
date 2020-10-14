from message.models import *
from django.test import TestCase
from message.utils import format_comment
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class GatewayTest(TestCase):
    def setUp(self):
        self.gateway = Gateway.objects.create(
            name="Africastalking",
            account_number="828299292",
            api_url="https://test.url",
            password="jkjfjdjkfjkdfjf",
            configured_sender="993939393",
            active=True,
        )
        self.message = Message.objects.create(
            gateway_id=self.gateway.id,
            status="SENT",
            partner_message_id="hjdhjdsjsjjsdjdsjjsd",
            status_code=201,
            recipient="+262829929292",
            response="test_message",
        )

    def test_gateway_str(self):
        self.assertEqual(
            str(self.gateway), u"{}{}".format(self.gateway.name, self.gateway.active)
        )

    def test_message_str(self):

        self.assertEqual(
            str(self.message), u"{}".format(self.message.partner_message_id)
        )

    def test_append_comment(self):
        comment = format_comment(self.message.response, "DLR", "test")
        expected_comment = u"{} {} [{}] {}".format("test_message", now, "DLR", "test")
        self.assertEqual(comment, expected_comment)
