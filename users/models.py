from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    father_name = models.CharField(
        'Отчество',
        max_length=50,
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True
    )
    image = models.ImageField(
        'Аватарка',
        upload_to='users/',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
# Create your models here.
