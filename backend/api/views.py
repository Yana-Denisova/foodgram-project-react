from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from djoser.views import UserViewSet
from fpdf import FPDF

from app.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow, User
from .paginations import CustomPagination
from .filters import CustomFilter
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          FollowerListSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer,)


class CustomUserViewset(UserViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        if request.user.is_anonymous:
            return Response('Пользователь не авторизован',
                            status=status.HTTP_401_UNAUTHORIZED)
        queryset = Follow.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowerListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FollowerListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='subscribe')
    def subscribe(self, request, id):
        if request.user.is_anonymous:
            return Response('Пользователь не авторизован',
                            status=status.HTTP_401_UNAUTHORIZED)
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
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeGetViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    pagination_class = PageNumberPagination
    filterset_class = CustomFilter

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
        if request.user.is_anonymous:
            return Response('Пользователь не авторизован',
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid()
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            if Favorite.objects.filter(recipe=recipe,
                                       subscriber=user).exists():
                return Response({
                    'errors': 'Рецепт уже есть в избранном'
                }, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(subscriber=user, recipe=recipe)
            return Response(f'Рецепт {recipe.name} добавлен в избранное',
                            serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, subscriber=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        if request.user.is_anonymous:
            return Response('Пользователь не авторизован',
                            status=status.HTTP_401_UNAUTHORIZED)
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.add_font('DejaVu',
                     fname='static/fonts/DejaVuSansMono.ttf', uni=True)
        pdf.set_font('DejaVu', size=16)
        shop = ShoppingCart.objects.filter(
            shopper=request.user).select_related('recipe').values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit').annotate(
                    amount=Sum('recipe__ingredient_amount'))
        for i in shop:
            pdf.cell(60, 20,
                     f"{i['recipe__ingredients__name']} {i['amount']} "
                     f"{i['recipe__ingredients__measurement_unit']}",
                     new_x="LMARGIN", new_y="NEXT")
        response = HttpResponse(
            bytes(pdf.output()), content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        return response

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        if request.user.is_anonymous:
            return Response('Пользователь не авторизован',
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShoppingCartSerializer(data=request.data)
        serializer.is_valid()
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    recipe=recipe, shopper=user).exists():
                return Response({
                    'errors': 'Такого рецепта нет в списке'
                }, status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = get_object_or_404(
                ShoppingCart, shopper=user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        ShoppingCart.objects.get_or_create(shopper=user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
