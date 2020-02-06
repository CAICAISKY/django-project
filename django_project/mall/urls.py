from django.urls import path, re_path

from mall import views


app_name = 'product'

urlpatterns = [
    # path('product_list/', views.product_list, name='product_list'),
    path('product_list/', views.ProduceListView.as_view(), name='product_list'),
    path('product_page_list/', views.ProduceListView.as_view(template_name='product_page_list.html'), name='product_page_list'),
    re_path(r'product_detail/(?P<pk>\S+)/$', views.product_detail, name='product_detail'),
    path('my_filter/', views.filter_test),
]
