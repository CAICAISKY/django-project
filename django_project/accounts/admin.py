from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ 用户模块 """
    list_display = ['username', 'nickname', 'integral', 'avatar']
