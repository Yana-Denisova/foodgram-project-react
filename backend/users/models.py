from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from django.db import models

#User = get_user_model()


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


#class Follow(models.Model):
    #"""Модель подписок"""
    #user = models.ForeignKey(
        #User,
        #on_delete=models.CASCADE,
        #related_name='follower',
        #verbose_name='Подписчик'
    #)
    #author = models.ForeignKey(
        #User,
        #on_delete=models.CASCADE,
        #related_name='following',
        #verbose_name='Автор'
    #)

    #class Meta:
        #constraints = [
            #models.UniqueConstraint(
                #fields=['user', 'author'], name='unique_follow'
            #)
        #]