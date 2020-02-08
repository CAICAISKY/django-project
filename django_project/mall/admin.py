from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.
from django import forms
from django.contrib import admin

from django_project.admin import set_invalid, set_valid
from mall.models import Product, Tag, Classify

admin.site.site_title = "后台管理页面"
admin.site.site_header = "商城后台管理"
admin.site.index_title = "欢迎您"


class ProductAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'origin_price']
    actions = [set_valid, set_invalid]
    form = ProductAdminForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['uid', 'code', 'name', 'img', 'is_valid']
    actions = [set_valid, set_invalid]


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    list_display = ['uid', 'code', 'name', 'desc', 'img', 'is_valid']
    actions = [set_valid, set_invalid]
