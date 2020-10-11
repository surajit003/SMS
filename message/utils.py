from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError


class ValidatePhoneNumber:
    def __call__(self, phone_number):
        if phone_number:
            phone_number = str(phone_number).strip()
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number
        try:
            validate_international_phonenumber(phone_number)
        except ValidationError as error:
            raise ValidationError(str(error))
        else:
            return phone_number
