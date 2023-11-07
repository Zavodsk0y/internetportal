import django
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from .validators import *


class AdvUser(AbstractUser):
    username = models.CharField(max_length=255, validators=[validate_latin], unique=True)
    fio = models.CharField(help_text='ФИО через пробел', max_length=128, validators=[validate_cyrillic])
    personal_data_agreement = models.BooleanField(default=False,
                                                  help_text='Согласие на обработку персональных данных')


class Category(models.Model):
    name = models.CharField(verbose_name='Категория заявки', max_length=255)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(help_text='Наименование заявки', max_length=255)
    description = models.TextField(help_text='Описание заявки')
    category = models.ForeignKey(Category, help_text='Категория заявки', on_delete=models.CASCADE)
    comment = models.TextField(help_text='Принимая заявку в работу, напишите комментарий об этом', default=None,
                               blank=True, null=True)

    APPLICATION_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('d', 'Выполнено')
    )

    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE)

    status = models.CharField(max_length=1, choices=APPLICATION_STATUS, blank=True, default='n',
                              help_text='Статус заявки')

    photo = models.ImageField(upload_to='media/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'bmp']),
                                          validate_file_size])

    date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.name
