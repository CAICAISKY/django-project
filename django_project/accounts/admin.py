from django.contrib import admin

from accounts.models import User
from django_project.admin import set_invalid, set_valid


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ 用户模块 """
    list_display = ['username', 'nickname', 'integral', 'avatar', 'is_valid']
    actions = [set_valid, set_invalid]
