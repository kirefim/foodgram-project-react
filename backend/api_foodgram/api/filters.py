from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters

from recipes.models import Recipe, Tag


class IngredientFilter(drf_filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorite', method='favorite_or_shopping_cart'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shoppingcart', method='favorite_or_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author']

    def favorite_or_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        filter_field = '__'.join([name, 'user'])
        return queryset.filter(**{filter_field: self.request.user.id})
