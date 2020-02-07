from django.contrib import messages


def disable_user(modeladmin, request, queryset):
    """ 逻辑关闭 """
    queryset.update(is_valid=False)
    messages.success(request, '关闭成功！')


def enable_user(modeladmin, request, queryset):
    """ 逻辑激活 """
    queryset.update(is_valid=True)
    messages.success(request, '激活成功！')


disable_user.short_description = '关闭'
enable_user.short_description = '激活'