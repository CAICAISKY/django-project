"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from django_project import settings, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mall/', include('mall.urls', namespace='mall')),
    path('index/', views.index, name='index'),
    path('', views.index),
    path('sys/', include('system.urls')),
    path('study/', include('django_study.urls')),
    path('accounts/', include('accounts.urls'))
]

urlpatterns += [
    re_path(r'^medias/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
