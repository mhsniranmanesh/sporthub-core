from django.core.validators import RegexValidator
from rest_framework.serializers import ValidationError
import re

class PhoneNumberValidator(object):
    def __init__(self):
        self.regex = re.compile('^(\+989[0-9]{2}\d{7})$')

    def __call__(self, value):
        if not self.regex.match(value):
            message = "Phone number must be in this format : +989xxxxxxxxx"
            raise ValidationError(message)


class NameValidator(object):
    def __init__(self):
        self.regex = re.compile('^[\u0600-\u06FF\s]+$')

    def __call__(self, value):
        if not self.regex.match(value):
            message = "Name must have only persian characters."
            raise ValidationError(message)
