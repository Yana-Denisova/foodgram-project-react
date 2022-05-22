from django.contrib import admin


from users.models import User, Follow

from .models import Tag, Ingredient, Recipe, IngredientAmount, Favorite

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')

admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')

admin.site.register(Ingredient, IngredientAdmin)


class IngredientAmountInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'image', 'name', 'text', 'cooking_time')
    inlines = (IngredientAmountInLine,)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Favorite)