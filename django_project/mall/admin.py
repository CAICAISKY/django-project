from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.
from django import forms
from django.contrib import admin

from mall.models import Product

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
    form = ProductAdminForm

