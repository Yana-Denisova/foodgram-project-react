from rest_framework import viewsets, status
from .serializers import TagSerializer, IngredientSerializer, RecipeGetSerializer, RecipePostSerializer
from app.models import Tag, Ingredient, Recipe, Favorite
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from .serializers import FollowerListSerializer, CustomUserSerializer, FavoriteSerializer
from django.shortcuts import get_object_or_404
from users.models import User, Follow
from rest_framework.response import Response
from rest_framework.decorators import action


class CustomUserViewset(UserViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        queryset = Follow.objects.all()
        serializer = FollowerListSerializer(queryset,  many=True)
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='subscribe')
    def subscribe(self, request, id):
        serializer = FollowerListSerializer(data=request.data)
        serializer.is_valid()
        author = get_object_or_404(User, pk=id)
        user = request.user
        if request.method == 'POST':
            if author == user:
                return Response({
                    'errors': 'Нельзя подписаться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.get_or_create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeGetViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeGetSerializer
        return RecipePostSerializer

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='favorite')
    def favorite(self, request, pk):
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid()
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            if Favorite.objects.filter(recipe=recipe, subscriber=user).exists():
                return Response({
                    'errors': 'Рецепт уже есть в избранном'
                }, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.get_or_create(subscriber=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, subscriber=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        pass
    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        pass

