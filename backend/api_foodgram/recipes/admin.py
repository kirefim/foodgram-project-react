from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInLine(admin.TabularInline):
    model = models.IngredientsRecipe


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    inlines = (IngredientsInLine,)
    empty_value_display = '-пусто-'

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ', '.join(ingredient.name for ingredient in obj.ingredients)

    @admin.display(description='Добавлений в избранное')
    def get_favorites_count(self, obj):
        return obj.favorites.count()


class FavoriteShoppingCart(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(models.Favorite)
class FavoriteAdmin(FavoriteShoppingCart):
    pass


@admin.register(models.ShoppingCart)
class ShoppingCartAdmin(FavoriteShoppingCart):
    pass
