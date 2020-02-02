from django.urls import path

from django_study import views

app_name = 'django_study'

urlpatterns = [
    path('test_ajax/', views.test_ajax, name='test_ajax'),
    path('ajax_html/', views.ajax_html, name='ajax_html')
]