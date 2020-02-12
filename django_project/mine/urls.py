from django.urls import path, re_path

from mine import views

app_name = 'mine'

urlpatterns = [
    re_path(r'^order_detail/(?P<sn>\S+)/$', views.OderDetailView.as_view(), name='order_detail'),
    re_path(r'^cart_add/(?P<product_uid>\S+)/$', views.cart_add, name='cart_add'),
    path('cart/', views.cart, name='cart')
]
