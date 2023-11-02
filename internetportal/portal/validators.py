import re

from django.core.exceptions import ValidationError


def validate_cyrillic(value):
    if not re.match(r'^[а-яА-ЯёЁ\s-]+$', value):
        raise ValidationError('Пожалуйста, используйте только кириллические буквы, дефис и пробелы.')


def validate_latin(value):
    if not re.match(r'^[a-zA-Z\s-]+$', value):
        raise ValidationError('Пожалуйста, используйте латиницу и дефис')
