
from django.core.exceptions import ValidationError


def mail_validator(mail):
    if not mail.endswith('gmail.com'):
        raise ValidationError('Daxil edilen email yanliz gmail hesabi olmalidir')
    return True