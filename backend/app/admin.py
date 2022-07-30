from django.contrib import admin

from users.models import Follow, User

from .models import (Favorite, Ingredient,
                     Recipe, ShoppingCart,
                     Tag, IngredientAmount)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')


class IngredientAmountInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text', 'cooking_time')
    inlines = (IngredientAmountInLine,)
    list_filter = ('tags', 'name')


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientAmount)
