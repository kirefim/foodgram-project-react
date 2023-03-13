from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as drf_views
from rest_framework import (
    permissions as drf_permissions, status, viewsets,)
from rest_framework.decorators import action
from rest_framework.response import Response

from . import filters, paginations, permissions, renderers, serializers
from recipes.models import (
    Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag)
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = (filters.IngredientFilter,)
    search_fields = ('^name',)


class UserViewSet(drf_views.UserViewSet):
    queryset = User.objects.all()
    pagination_class = paginations.CustomPagnation

    @action(['post', 'delete'], detail=True,
            permission_classes=[drf_permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            serializer = serializers.FollowSerializer(
                data={'user': request.user.id, 'author': id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        get_object_or_404(Follow, user=request.user, author=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[drf_permissions.IsAuthenticated])
    def subscriptions(self, request):
        instance = (User.objects.filter(following__user=request.user)
                    .prefetch_related('recipes'))
        page = self.paginate_queryset(instance)
        serializer = serializers.FollowerSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = (Recipe.objects.select_related('author')
                .prefetch_related('ingredients', 'tags')
                .prefetch_related('favorite', 'shoppingcart'))
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthorOrReadOnly]
    pagination_class = paginations.CustomPagnation
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RecipeFilter

    def get_serializer_class(self):
        if self.request.method in drf_permissions.SAFE_METHODS:
            return super().get_serializer_class()
        return serializers.RecipeCreateSerializer

    def _post_delete_action(self, request, serializer, model):
        recipe = self.get_object()
        if request.method == 'POST':
            serializer = serializer(
                data={'user': request.user.id, 'recipe': recipe.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(model, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post', 'delete'], detail=True,
            permission_classes=[drf_permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        serializer = serializers.FavoriteSerializer
        return self._post_delete_action(request, serializer, Favorite)

    @action(['post', 'delete'], detail=True,
            permission_classes=[drf_permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        serializer = serializers.ShoppingCartSerializer
        return self._post_delete_action(request, serializer, ShoppingCart)

    @action(detail=False, renderer_classes=[renderers.PDFRenderer],
            permission_classes=[drf_permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = (
            Ingredient.objects.filter(recipes__shoppingcart__user=request.user)
            .order_by('name').annotate(
                amount=Sum('ingredients_recipe__amount')
                )
        )
        return Response(ingredients)
