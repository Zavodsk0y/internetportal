import re

from django.core.exceptions import ValidationError


def validate_cyrillic(value):
    if not re.match(r'^[а-яА-ЯёЁ\s-]+$', value):
        raise ValidationError('Пожалуйста, используйте только кириллические буквы, дефис и пробелы')


def validate_latin(value):
    if not re.match(r'^[a-zA-Z\s-]+$', value):
        raise ValidationError('Пожалуйста, используйте латиницу и дефис')


def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError("Размер загруженного файла превышает 2Мб")
    else:
        return value
