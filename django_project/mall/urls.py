from django.urls import path, re_path

from mall import views


app_name = 'product'

urlpatterns = [
    # path('product_list/', views.product_list, name='product_list'),
    # 商品列表页
    path('product_list/', views.ProduceListView.as_view(), name='product_list'),
    # 商品列表加载部分
    path('product_page_list/', views.ProduceListView.as_view(template_name='product_page_list.html'), name='product_page_list'),
    # 商品详情
    re_path(r'product_detail/(?P<uid>\S+)/$', views.product_detail, name='product_detail')
]
