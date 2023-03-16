from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'get_followers_count', 'get_recipes_count')
    search_fields = ('email', 'username')
    list_filter = ('username',)
    empty_value_display = '-пусто-'

    @admin.display(description='Подписчиков')
    def get_followers_count(self, obj):
        return obj.following.count()

    @admin.display(description='Рецептов')
    def get_recipes_count(self, obj):
        return obj.recipes.count()
