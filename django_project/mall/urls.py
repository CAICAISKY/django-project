from django.urls import path, re_path

from mall import views


app_name = 'product'

urlpatterns = [
    path('prod/list/', views.product_list, name='product_list'),
    re_path(r'prod/detail/(?P<pk>\S+)/$', views.product_detail, name='product_detail'),



    path('my_filter/', views.filter_test),
]