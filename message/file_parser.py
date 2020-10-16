from message.models import FileUpload
import csv
from africastalking.utils import send_sms_via_at
import logging
import hashlib

logger = logging.getLogger(__name__)


class Upload:
    def __init__(self, file_id):
        self.file_id = file_id
        self.error = []
        self.valid_row = []

    def validate_file_tag(self, tag):
        pass

    def validate_header(self, header):
        pass

    def __parse(self, reader):
        pass

    def errors(self):
        if len(self.error) > 0:
            return self.error
        else:
            return


class BulkSMSUpload(Upload):
    def validate_file_tag(self, tag):
        if tag == "bulk_sms":
            return True

    def __parse(self, reader):
        line_number = 3
        for row in reader:
            if "" in row:
                row_dict = {}
                row_dict["line_number"] = line_number
                row_dict["row"] = row
                self.error.append(row_dict)
            else:
                self.valid_row.append(row)

            line_number += 1

    def trigger_sms(self):
        log_prefix = "TRIGGER SMS"
        try:
            file = FileUpload.objects.get(id=self.file_id)
            with open(file.document.path, "r") as f:
                reader = csv.reader(f)
                _tag = next(reader)
                _tag = "".join(_tag)
                if self.validate_file_tag(_tag):
                    header = next(reader)
                    if self.validate_headers(header):
                        self.__parse(reader)
            if len(self.valid_row) > 0:
                self.send_sms(self.valid_row)  # can be a celery process

        except FileUpload.DoesNotExist as ex:
            logger.exception("{} {}".format(log_prefix, ex))
            return
        except Exception as ex:
            logger.exception("{} {}".format(log_prefix, ex))
            return

    def validate_headers(self, header):
        expected_header = ["contact_number", "name", "message"]
        if set(expected_header) == set(header):
            return True

    def flood_control(self,phone_number,message):
        val = str(phone_number)+str(message)
        cache_key = hashlib.md5(val.encode('utf-8')).hexdigest()
        from django.core.cache import cache
        if cache.get(cache_key):
            # Possible duplicate
            raise Exception("Duplicate SMS to {} detected: {}".format(str(phone_number), message))
        else:
            # Cache for for 1 hour
            cache.set(cache_key, True, 3600)
            return True

    def send_sms(self, row):
        for data in row:
            if self.flood_control(data[0],data[2]):
                send_sms_via_at(
                    [data[0]], data[2], "sandbox", data[1]
                )  # can be a celery process
