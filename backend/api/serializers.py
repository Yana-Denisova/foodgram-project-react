from email.mime import image
from rest_framework import serializers
from app.models import Tag, Ingredient, Recipe, IngredientAmount, Favorite
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from users.models import User, Follow
from djoser.serializers import UserSerializer

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
        fields = ('id','name', 'image','cooking_time')

class ImageField(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        image = Base64ImageField()
        return image

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    def get_is_subscribed(self, obj):
        if Follow.objects.filter(author=obj.id).exists():
            return True
        return False
    class Meta:
        fields =('email', 'id', 'username', 'first_name', 'last_name','is_subscribed')
        model = User

    
class FollowerListSerializer(UserSerializer):
    email = serializers.CharField(source='author.email')
    id = serializers.CharField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = RecipeSerializer(source ='author.recipes', many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    def get_recipes_count(self, obj):
        author_id = obj.author.id
        return Recipe.objects.filter(author=author_id).count()
    
    def get_is_subscribed(self,obj):
        if Follow.objects.filter(author=obj.author, user=obj.user).exists():
            return True

    class Meta:
        model = Follow
        fields= ('email', 'id', 'username', 'first_name', 'last_name','is_subscribed', 'recipes', 'recipes_count')


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
    image = ImageField()                                 
    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredient_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            ingredient_id = ingredient['ingredients']['id']
            ingredient_amount=ingredient['amount']
            current_ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
            IngredientAmount.objects.create(
                ingredients=current_ingredient, recipe=recipe, amount=ingredient_amount)
        return recipe 


class RecipeGetSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountSerializerGet(
        source='ingredient_amount',
        many=True,
        read_only=True)
    tags = TagSerializer(
        many=True,
        read_only=True)                             
    
    class Meta:
        model = Recipe
        fields = ('id','tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.CharField(source='recipe.image')
    cooking_time = serializers.CharField(source='recipe.cooking_time')
    class Meta:
        model = Favorite
        fields = ('id','name', 'image','cooking_time')