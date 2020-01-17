from django.urls import path

from learn_test import views

app_name = "test"

urlpatterns = [
    path("test_one/", views.test_one, name="test_one"),
    path("test_two/", views.test_two, name="test_two"),
]