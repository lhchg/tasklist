"""
URL configuration for analyze project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import views, upload
from django.urls import re_path as url
from django.views.static import serve
from . import settings

from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.runoob),
    path('tips', views.tips),
    path('normal', views.runoob_normal),
    url(r'^create_task/$', views.create_task),
    path('upload/<path:path>/', serve, {'document_root': settings.MODEL_ROOT}),
    path('result/<path:path>/', serve, {'document_root': settings.RESULT_ROOT}),
    path('exe/<path:path>/', serve, {'document_root': settings.EXE_ROOT}),
    path('layui/<path:path>/', serve, {'document_root': settings.LAYUI_ROOT}),
    path('resource/<path:path>/', serve, {'document_root': settings.RESOURCE_ROOT}),
    path('start_upload_service/', upload.start_upload_service, name='start_upload_service'),
    path('get_uploaded_filename/', upload.get_uploaded_filename, name='get_uploaded_filename'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
