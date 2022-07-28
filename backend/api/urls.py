from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewset, IngredientViewSet, RecipeGetViewSet,
                    TagViewSet)

router = DefaultRouter()
router.register('users', CustomUserViewset)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeGetViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
