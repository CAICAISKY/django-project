# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from mall.models import Product
from mine.models import Order, Cart
from utils import constants


class OderDetailView(LoginRequiredMixin, DetailView):
    """ 订单详情视图 """
    model = Order
    template_name = 'order_info.html'
    slug_url_kwarg = 'sn'
    slug_field = 'sn'
    context_object_name = 'order'


@login_required
@transaction.atomic()
def cart_add(request, product_uid):
    """ 添加到购物车 """
    # 获取对应的商品
    product = get_object_or_404(Product, uid=product_uid, is_valid=True, status=constants.PRODUCT_STATUS_SELL)
    # 获取添加的商品数量
    count = int(request.POST.get('count', 1))
    # 进行商品库存验证
    if product.ramain_count < count:
        return HttpResponse('库存不足！')
    # 减少商品库存
    product.update_store_count(count)
    try:
        # 当前用户有购过该商品时，获取购物车，并进行数据修改
        cart = Cart.objects.get(status=constants.ORDER_STATUS_INIT, user=request.user, product=product)
        count = cart.count + count
        cart.count = count
        cart.amount = cart.price * count
        cart.save()
    except Cart.DoesNotExist:
        # 当前用户没有购物车时，新建购物车
        Cart.objects.create(
            user=request.user,
            product=product,
            name=product.name,
            img=product.img,
            price=product.price,
            origin_price=product.origin_price,
            count=count,
            amount=product.price * count
        )
    return HttpResponse('ok')
