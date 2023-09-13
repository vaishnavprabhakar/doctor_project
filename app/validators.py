from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError


def validate_username(username):
    username = username
    if username.isalnum():
        raise ValidationError("username must contain alphanumeric charectors.")
    return username