from django.urls import path, re_path

from mine import views

app_name = 'mine'

urlpatterns = [
    # 订单详情
    re_path(r'^order_detail/(?P<sn>\S+)/$', views.OderDetailView.as_view(), name='order_detail'),
    # 添加购物车
    re_path(r'^cart_add/(?P<product_uid>\S+)/$', views.cart_add, name='cart_add'),
    # 购物车商品数量查询
    path('cart_count/', views.cart_count, name='cart_count'),
    # 购物车
    path('cart/', views.cart, name='cart'),
    # 订单支付
    path('order_pay/<int:sn>', views.order_pay, name='order_pay'),
    # 订单列表
    path('order_list/<int:status>', views.OrderListView.as_view(), name='order_list'),
    # 删除订单
    path('order_delete/', views.order_delete, name='order_delete'),
    # 个人中心
    path('mine/', views.mine, name='mine'),
    # 收藏
    path('product_collect/', views.product_collect, name='product_collect')
]
