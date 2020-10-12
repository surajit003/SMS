from message.models import Gateway, Message
from message.utils import ValidatePhoneNumber
import logging
import requests
import json

logger = logging.getLogger(__name__)


def validate_recipients(recipient):
    validate_phone = ValidatePhoneNumber()
    valid_nos = []
    if isinstance(recipient, list):
        for number in recipient:
            if validate_phone(number):
                valid_nos.append(number)
        return valid_nos


def send_sms_via_at(recipient, message, account_name=None):
    log_prefix = "SEND SMS VIA AT"
    if len(validate_recipients(recipient)) != 0:
        recipient = validate_recipients(recipient)
        recipient = ",".join(recipient)
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
            data = {
                "username": gateway.account_number,
                "to": recipient,
                "message": message,
            }

            headers = {
                "apikey": gateway.password,
                "content-type": "application/x-www-form-urlencoded",
                "accept": "application/json",
            }
            response = requests.post(gateway.api_url, headers=headers, data=data)
            logger.info("{}-{}".format(log_prefix, response))
            if response.status_code == 201:
                parse_and_save_response(json.loads(response.content)) #make it a celery task recommended
            return response
    else:
        return


def parse_and_save_response(response):
    log_prefix = 'PARSE AND SAVE RESPONSE'
    logging.info('{} {}'.format(log_prefix,response))
    try:
        messagedata = response['SMSMessageData']
        recipients = messagedata['Recipients']
        gateway = Gateway.objects.get(name='Africastalking')
        for recipient in recipients:
            status_code = int(recipient['statusCode'])
            receiver = recipient['number']
            status = recipient['status']
            message_id = recipient['messageId']
            message = Message(gateway=gateway, status_code=status_code, recipient=receiver,
                              status=status, partner_message_id=message_id
                              )
            message.append_comment('DLR', response)
            message.save()
    except KeyError as ex:
        logger.exception('{} {} {}'.format(log_prefix,'Missing Key', ex))
