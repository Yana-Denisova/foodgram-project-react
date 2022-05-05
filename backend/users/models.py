from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.db import models

#class User(AbstractUser):
    #email = models.EmailField(
        #max_length=254, unique=True, blank=False,
        #null=False, verbose_name='Адрес электронной почты')
    #username = models.CharField(
        #max_length=150, validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        #unique=True, blank=False, null=False, verbose_name='Уникальный юзернейм')
    #first_name = models.CharField(
        #max_length=150, blank=False, null=False, verbose_name='Имя')
    #last_name = models.CharField(
        #max_length=150, blank=False, null=False, verbose_name='Фамилия')
    #password = models.CharField(
        #max_length=150, blank=False, null=False, verbose_name=' Пароль')

    #class Meta:
        #ordering = ['username']
        #verbose_name = 'пользователь'
        #verbose_name_plural = 'пользователи'

    #def __str__(self):
        #return self.username
