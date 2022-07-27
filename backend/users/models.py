from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.db import models


class User(AbstractUser):
    """Кастомизированная модель юзера"""
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='dont_follow_yourself')
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на себя')
