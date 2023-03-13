from django.core import validators
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_hex


class Ingredient(models.Model):
    name = models.CharField(
        'Ингредиент', max_length=settings.DEFAULT_MAX_LENGTH,)
    measurement_unit = models.CharField(
        'Единицы измерения', max_length=settings.DEFAULT_MAX_LENGTH,)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Тэг', max_length=settings.DEFAULT_MAX_LENGTH, unique=True)
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        validators=[validate_hex]
    )
    slug = models.SlugField(
        'Ссылка на тэг', max_length=settings.DEFAULT_MAX_LENGTH,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        db_index=True,
    )
    name = models.CharField(
        'Название рецепта',
        max_length=settings.DEFAULT_MAX_LENGTH,
        unique=True
    )
    image = models.ImageField(
        'Ссылка на картинку', upload_to='recipes/', unique=True)
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        verbose_name='Список ингредиентов',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тэгов',
        related_name='recipes',
        db_index=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            validators.MinValueValidator(
                limit_value=settings.DEFAULT_MIN_VALUE,
                message='Время приготовления не может быть менее 1 минуты'
            )
        ],
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True,)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_recipe'
            ),
            models.UniqueConstraint(
                fields=['name', 'image'],
                name='unique_name_image'
            ),
        ]

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        blank=False,
        null=False,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            validators.MinValueValidator(
                limit_value=settings.DEFAULT_MIN_VALUE,
                message='Количество не может быть менее 1'
            )
        ]
    )


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = "Подписки"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow')
        ]


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        db_index=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(class)s_recipe_unique')
        ]

    def __str__(self):
        return f'{_(self.__class__.__name__)} {self.user.get_username()}'


class Favorite(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        verbose_name = "Избранное юзера"
        verbose_name_plural = "Избранное"
        default_related_name = 'favorite'


class ShoppingCart(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        default_related_name = 'shoppingcart'
