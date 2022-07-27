from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db import IntegrityError
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
from .permissions import AuthorOrReadOnly
from .paginations import CustomPagination
from .filters import CustomFilter
from .serializers import (CustomUserSerializer, TagSerializer,
                          FollowerListSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          AddFavoriteSerializer, RecipeSerializer,
                          AddShoppingCartSerializer)


class CustomUserViewset(UserViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=False, url_path='subscriptions',
            permission_classes=(AuthorOrReadOnly,))
    def subscriptions(self, request):
        queryset = Follow.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowerListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FollowerListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='subscribe', permission_classes=(AuthorOrReadOnly,))
    def subscribe(self, request, id):
        serializer = FollowerListSerializer(data=request.data)
        serializer.is_valid()
        author = get_object_or_404(User, pk=id)
        user = request.user
        if request.method == 'POST':
            try:
                Follow.objects.get_or_create(user=user, author=author)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response('Нельзя подписаться на себя',
                                status=status.HTTP_400_BAD_REQUEST)
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

    def add_obj(self, request, pk, my_serializer, my_model):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        data = {}
        data['recipe'] = recipe.pk
        data['subscriber'] = user.pk
        if request.method == 'POST':
            serializer = my_serializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = RecipeSerializer(
                            recipe, context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        obj = get_object_or_404(my_model, subscriber=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='favorite')
    def favorite(self, request, pk):
        return self.add_obj(request, pk,
                            my_serializer=AddFavoriteSerializer,
                            my_model=Favorite)

    @action(
        methods=['POST', 'DELETE'], detail=True,
        url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        return self.add_obj(request, pk,
                            my_serializer=AddShoppingCartSerializer,
                            my_model=ShoppingCart)

    @action(detail=False, url_path='download_shopping_cart',
            permission_classes=(AuthorOrReadOnly,))
    def download_shopping_cart(self, request):
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
