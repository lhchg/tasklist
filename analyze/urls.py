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
from . import views
from django.urls import re_path as url
from django.views.static import serve
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.runoob),
    url(r'^create_task/$', views.create_task),
    path('upload/<path:path>/', serve, {'document_root': settings.MODEL_ROOT}),
    path('result/<path:path>/', serve, {'document_root': settings.RESULT_ROOT}),
]
