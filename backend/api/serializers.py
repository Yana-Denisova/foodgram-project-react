from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import Follow, User
from app.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                        ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(author=obj.id).exists()

    class Meta:
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        model = User


class FollowerCreateSerializer(UserSerializer):
    class Meta:
        model = Follow
        fields = ('author', 'user')

    def validate(self, data):
        if data['author'] == data['user']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя')
        return data


class FollowerListSerializer(UserSerializer):
    email = serializers.CharField(source='author.email')
    id = serializers.CharField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = RecipeSerializer(source='author.recipes', many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        author_id = obj.author.id
        return Recipe.objects.filter(author=author_id).count()

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(author=obj.author, user=obj.user).exists()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')


class AmountSerializerGet(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredients.name')
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AmountSerializerPost(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    ingredients = AmountSerializerPost(
        source='ingredient_amount',
        many=True,)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('image',)

    def validate_tags(self, value):
        tags_list = []
        for tag in value:
            if not tag:
                raise serializers.ValidationError(
                    'Необходимо указать теги')
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Нельзя указывать 2 одинаковых ингредиента')
            tags_list.append(tag)
        return value

    def validate(self, data):
        ingredients = data['ingredient_amount']
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо ввести ингредиенты')
        ingredients_list = []
        for ingredient_value in ingredients:
            ingredient_id = ingredient_value['ingredients']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'Ингридиенты должны быть уникальными')
            ingredients_list.append(ingredient_id)
            if int(ingredient_value['amount']) <= 0:
                raise serializers.ValidationError(
                    'Значение количества должно быть больше 0')
        return data

    def add_ingredients(self, ingredients_list, recipe):
        return IngredientAmount.objects.bulk_create([IngredientAmount(
                ingredients=get_object_or_404(
                                Ingredient,
                                pk=ingredient['ingredients']['id']),
                recipe=recipe,
                amount=ingredient['amount'])
                for ingredient in ingredients_list])

    def create(self, validated_data, *args):
        ingredients_list = validated_data.pop('ingredient_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients_list, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        ingredients_list = validated_data.pop('ingredient_amount')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.add_ingredients(ingredients_list, recipe=instance)
        return super().update(instance, validated_data)


class RecipeGetSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountSerializerGet(
        source='ingredient_amount',
        many=True,
        read_only=True)
    tags = TagSerializer(
        many=True,
        read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return Favorite.objects.filter(
            subscriber=user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return ShoppingCart.objects.filter(
            subscriber=user.id, recipe=obj.id).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.CharField(source='recipe.image')
    cooking_time = serializers.CharField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.CharField(source='recipe.image')
    cooking_time = serializers.CharField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'cooking_time')


class AddFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', 'subscriber')

    def validate(self, data):
        recipe = data['recipe']
        subscriber = data['subscriber']
        if Favorite.objects.filter(
            recipe=recipe,
            subscriber=subscriber
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное')
        return data


class AddShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('recipe', 'subscriber')

    def validate(self, data):
        recipe = data['recipe']
        subscriber = data['subscriber']
        if ShoppingCart.objects.filter(
            recipe=recipe,
            subscriber=subscriber
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в cписок покупок')
        return data
