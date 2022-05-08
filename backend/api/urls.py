from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngredientViewSet, RecipeGetViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipe',RecipeGetViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
