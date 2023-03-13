from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from recipes.models import (
    Favorite, Follow, Ingredient,
    IngredientsRecipe, Recipe, ShoppingCart, Tag,
    )
from users.models import User


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return obj.following.filter(user=request.user).exists() if (
            request and not request.user.is_anonymous) else False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['name']


class IngredientsRecipeSerializer(IngredientSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='ingredient.id'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = IngredientsRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class CreateIngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects,)

    class Meta:
        model = IngredientsRecipe
        fields = ['id', 'amount']


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = CreateIngredientsRecipeSerializer(many=True,)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects)
    image = Base64ImageField(
        validators=[validators.UniqueValidator(Recipe.objects.all())]
    )

    class Meta:
        model = Recipe
        fields = [
            'author', 'tags', 'ingredients', 'name',
            'image', 'text', 'cooking_time',
        ]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name'),
                message='Вы уже постили данный рецепт'
            ),
            validators.UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('image', 'name'),
                message='Рецепт с таким именем и картинкой уже существует'
            ),
        ]

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 1'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Вы не указали ни одного ингредиента'
            )
        unique_values = []
        for ingredient in value:
            for unique_value in unique_values:
                if ingredient.get('id') == unique_value.get('id'):
                    raise serializers.ValidationError(
                        'Ингредиенты должны быть уникальны'
                    )
            unique_values.append(ingredient)
            if ingredient.get('amount') < 1:
                id = ingredient.get('id')
                raise serializers.ValidationError(
                    f'Количество ингредиента c id {id} должно быть бальше 0'
                )
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Вы не указали ни одного тэга'
            )
        unique_values = set(value)
        if len(value) != len(unique_values):
            raise serializers.ValidationError(
                'Тэги должны быть уникальны'
            )
        return value

    @staticmethod
    def create_ingredients(recipe, ingredients):
        return IngredientsRecipe.objects.bulk_create(
            [
                IngredientsRecipe(
                    recipe=recipe,
                    ingredient=ingredient.pop('id'),
                    amount=int(ingredient.pop('amount')),
                ) for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.set(validated_data.pop('tags'), clear=True)
        instance.ingredients.clear()
        self.create_ingredients(instance, validated_data.pop('ingredients'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True,)
    tags = TagSerializer(many=True,)
    ingredients = IngredientsRecipeSerializer(
        many=True, source='ingredients_recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'tags', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return obj.favorite.filter(user=request.user).exists() if (
            request and not request.user.is_anonymous) else False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return obj.shoppingcart.filter(user=request.user).exists() if (
            request and not request.user.is_anonymous) else False


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class FavoriteShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}).data


class FavoriteSerializer(FavoriteShoppingCartSerializer):
    class Meta(FavoriteShoppingCartSerializer.Meta):
        model = Favorite
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class ShoppingCartSerializer(FavoriteShoppingCartSerializer):
    class Meta(FavoriteShoppingCartSerializer.Meta):
        model = ShoppingCart
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]


class FollowerSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes_count', 'recipes']
        read_only_fields = [
            'email', 'username', 'firstname', 'lastname',
            'is_subscribed', 'recipe', 'recipe_count']

    @staticmethod
    def _recipe_limit_validate(value):
        try:
            return int(value)
        except TypeError:
            raise serializers.ValidationError(
                'Количество рецептов на странице должно быть целым числом')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = (self.context['request'].query_params
                         .get('recipes_limit'))
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:self._recipe_limit_validate(recipes_limit)]
        return RecipeShortSerializer(recipes, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        exclude = ('id',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Такая подписка уже существует!'
            )
        ]

    def validate_author(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return value

    def to_representation(self, instance):
        return FollowerSerializer(instance.author, context=self.context).data
