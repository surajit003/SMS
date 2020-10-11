from message.models import Gateway
from message.utils import ValidatePhoneNumber
import logging
import requests
import json

logger = logging.getLogger(__name__)


def send_sms_via_at(recipient, message, account_name=None):
    log_prefix = "SEND SMS VIA AT"
    validate_phone = ValidatePhoneNumber()
    if validate_phone(recipient):
        try:
            if account_name:
                gateway = Gateway.objects.get(
                    name="Africastalking", account_name=account_name, active=True
                )
            else:
                gateway = Gateway.objects.get(name="Africastalking", active=True)
        except Gateway.DoesNotExist as ex:
            raise Exception("Gateway is not set up for recipient {}".format(recipient))
        except Gateway.MultipleObjectsReturned:
            raise Exception("Multiple Gateway found for {}".format(recipient))
        else:
            data = json.dumps(
                {
                    "username": gateway.account_number,
                    "to": [recipient],
                    "message": message,
                    "from": gateway.configured_sender,
                }
            )
            headers = {
                "apikey": str(gateway.password),
                "content-type": "application/json",
            }
            response = requests.post(gateway.api_url, headers=headers, data=data)
            logger.info("{}-{}".format(log_prefix, response))
            return response

    else:
        raise Exception
