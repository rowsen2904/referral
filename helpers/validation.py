import re

from django.core.exceptions import ValidationError


def validate_russian_phone(value):
    if not re.fullmatch(r'^\+7\d{10}$', value):
        raise ValidationError("The number must be in the format: +7XXXXXXXXXX")
    return value
