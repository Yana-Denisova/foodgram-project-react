from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(
        max_length=150, unique=True, blank=False,
        null=False, verbose_name='Название тега')
    color = models.CharField(
        unique=True, blank=False,
        null=False, verbose_name='Цвет тега')
    slug = models.CharField(
        max_length=150, unique=True, blank=False,
        null=False, verbose_name='Слаг')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,  db_index=True,
        verbose_name='Ингредиент')
    measurement_unit = models.CharField(
        max_length=25, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name

class Amount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name='amount',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        verbose_name='Количество в рецепте')
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Amount, related_name='ingredient',
        verbose_name='Ингредиент',
        db_index=True,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes',
        verbose_name='Тег', db_index=True)
    image = models.CharField(
        verbose_name='Изображение')
    name = models.CharField(
        max_length=200,  db_index=True,
        verbose_name='Название')
    text = models.TextField(
        verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, 'Минимальное время приготовления 1 минута'),
        ])
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name



class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_favorite'
            )
        ] 