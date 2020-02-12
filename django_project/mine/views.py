# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView

from mall.models import Product
from mine.models import Order, Cart
from utils import constants
from utils.tools import get_trans_id


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


@login_required
@transaction.atomic()
def cart(request):
    """ 购物车视图 """
    # 获取当前用户仍放在购物车中的商品列表
    user = request.user
    cart_list = user.user_carts.filter(status=constants.ORDER_STATUS_INIT)
    if request.method == 'POST':
        # 获取默认地址，如果没有地址，跳转到地址列表
        default_address = user.default_address
        if not default_address:
            messages.warning(request, '请先填写送货地址')
            return redirect('accounts:address_list')
        # 计算订单总额
        cart_total = cart_list.aggregate(sum_amount=Sum('amount'), sum_count=Sum('count'))
        # 创建订单
        order = Order.objects.create(
            sn=get_trans_id(),
            user=user,
            to_user=default_address.username,
            to_area=default_address.get_region(),
            to_address=default_address.address,
            to_phone=default_address.phone,
            buy_count=cart_total['sum_count'],
            buy_amount=cart_total['sum_amount']
        )
        # 修改购物车中商品的状态为已提交
        cart_list.update(
            status=constants.ORDER_STATUS_SUBMIT,
            order=order
        )
        messages.success(request, '下单成功，请支付')
        return redirect('mine:order_detail', order.sn)

    return render(request, 'cart.html', {
        'cart_list': cart_list
    })
