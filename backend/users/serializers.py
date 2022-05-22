
from rest_framework import serializers
from .models import Follow
from django.contrib.auth import get_user_model
from .models import User
#User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализаци для пользователя"""
    class Meta:
        model = User
        fields = ('email','id','username','first_name','last_name','is_subscribed')


class FollowerListSerializer(serializers.ModelSerializer):
    """Сериализация списка подписок с выдачей рецептов"""
    author = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Follow
        fields = ('author',)

class AddFollowSerializer(serializers.ModelSerializer):
    """Добавление в подписки"""