from django.contrib import admin

from accounts.models import User, UserAddress
from django_project.admin import set_invalid, set_valid


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ 用户后台管理 """
    list_display = ['username', 'nickname', 'integral', 'avatar', 'is_valid']
    actions = [set_valid, set_invalid]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """ 地址后台管理 """
    actions = [set_valid, set_invalid]
