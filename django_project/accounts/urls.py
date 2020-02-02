from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
]