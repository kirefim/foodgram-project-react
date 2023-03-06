from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_foodgram.settings import (
    DEFAULT_MAX_LENGTH_EMAIL, DEFAULT_MAX_LENGTH_USER_FIEELD)


class User(AbstractUser):

    email = models.EmailField(
        'Электронная почта',
        max_length=DEFAULT_MAX_LENGTH_EMAIL,
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=DEFAULT_MAX_LENGTH_USER_FIEELD,
        unique=True,
        db_index=True,
        validators=[UnicodeUsernameValidator(
            message='Введите корректное имя пользователя'
            )
        ],
        help_text='Разрешены латинские буквы, цифры, символы: @/./+/-/_'
    )
    first_name = models.CharField(
        'Имя', max_length=DEFAULT_MAX_LENGTH_USER_FIEELD,
    )
    last_name = models.CharField(
        'Фамилия', max_length=DEFAULT_MAX_LENGTH_USER_FIEELD,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'
