from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    list_filter = ('username',)
    empty_value_display = '-пусто-'
