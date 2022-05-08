from django.contrib import admin

from .models import Tag, Ingredient, Recipe

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')

admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')

admin.site.register(Ingredient, IngredientAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'image', 'name', 'text', 'cooking_time')
    filter_horizontal = ('tags', 'ingredients')
admin.site.register(Recipe, RecipeAdmin)