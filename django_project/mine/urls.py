from django.urls import path, re_path

from mine import views

app_name = 'mine'

urlpatterns = [
    re_path(r'^order_detail/(?P<sn>\S+)/$', views.OderDetailView.as_view(), name='order_detail')
]
