from django.urls import path

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
    path("password_change/", views.password_change, name='password_change')
]