from django.urls import path

from system import views

app_name = 'system'

urlpatterns = [
    path('news_info/<int:pk>', views.news_info, name='news_info'),
    path('news_list/', views.news_list, name='news_list')
]
