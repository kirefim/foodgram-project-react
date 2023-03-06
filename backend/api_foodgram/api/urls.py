from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, 'tags')
router.register('ingredients', views.IngredientViewSet, 'ingredients')
router.register('recipes', views.RecipeViewSet, 'recipes')
router.register('users', views.UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
