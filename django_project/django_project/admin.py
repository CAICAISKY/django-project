""" 设置公用的后台管理操作 """
from django.contrib import messages


def set_valid(modeladmin, request, queryset):
    """ 激活 """
    queryset.update(is_valiid=True)
    messages.success('激活成功！')


def set_invalid(modeladmin, request, queryset):
    """ 关闭 """
    queryset.update(is_valiid=False)
    messages.success('关闭成功！')


set_valid.short_description = '有效'
set_invalid.short_description = '无效'
