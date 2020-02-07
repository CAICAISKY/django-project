from django.contrib import admin

# Register your models here.
from mine.models import Order, Cart, Comments


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ 订单后台管理 """
    list_display = ['sn', 'user', 'to_user', 'to_area', 'to_address', 'to_phone']
    search_fields = ['user__nickname', 'user__username', 'to_user']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ 购物车后台管理 """
    list_display = ['name', 'user', 'price', 'img']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """ 商品评价后台管理 """
    list_display = ['user', 'product', 'score', 'desc']
