from django.contrib import admin

from django_project.admin import set_valid, set_invalid
from system.models import Slider, News, ImageFile


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """ 轮播图后台管理 """
    list_display = ['name', 'desc', 'img', 'types', 'start_time', 'end_time', 'is_valid']
    actions = [set_valid, set_invalid]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """ 新闻通知后台管理 """
    list_display = ('title', 'types', 'is_valid')
    actions = [set_valid, set_invalid]


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    """ 图片库后台管理 """
    list_display = ('summary', 'img', 'content_type', 'is_valid')
    actions = [set_valid, set_invalid]
