from django.urls import path, re_path

from accounts import views

app_name = "accounts"

urlpatterns = [
    # 登录
    path("login/", views.user_login, name="user_login"),
    # 退出
    path("logout/", views.user_logout, name="user_logout"),
    # 注册
    path("register/", views.user_register, name="user_register"),
    # 密码修改
    path("password_change/", views.password_change, name='password_change'),
    # 地址列表
    path("address_list/", views.address_list, name='address_list'),
    # 地址编辑/新增
    re_path(r"^address_edit/(?P<pk>\S+)/$", views.address_edit, name='address_edit'),
    # 地址删除
    re_path(r'^address_delete/(?P<pk>\S+)/$', views.address_delete, name='address_delete')
]
