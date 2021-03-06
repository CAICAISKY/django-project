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
    # 首页
    path('', views.index),
    path('index/', views.index, name='index'),
    # 商品模块
    path('mall/', include('mall.urls')),
    # 系统模块
    path('sys/', include('system.urls')),
    # 用户模块
    path('accounts/', include('accounts.urls')),
    # 个人模块
    path('mine/', include('mine.urls')),
    path('study/', include('django_study.urls')),

]

urlpatterns += [
    # django文件上传路径配置
    re_path(r'^medias/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }),
    # ckeditor图片上传路径配置
    re_path(r'ckeditor/', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
