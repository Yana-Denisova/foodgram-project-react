from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=150, unique=True,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Цвет тега')
    slug = models.CharField(
        max_length=150, unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, db_index=True,
        verbose_name='Ингредиент')
    measurement_unit = models.CharField(
        max_length=25, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиент',
        db_index=True,
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes',
        verbose_name='Тег', db_index=True)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=200, db_index=True,
        verbose_name='Название')
    text = models.TextField(
        verbose_name='Текст рецепта')
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


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amount')
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_amount'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredients', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return str(self.amount)


class Favorite(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Shopping',
        verbose_name='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Shopping',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'recipe'],
                name='unique_shopper_recipe'
            )
        ]

    def __str__(self):
        return self.recipe.name
