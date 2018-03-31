"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.conf import settings
from main import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('create_event', views.create_event, name="create_event"),
    path('add_event', views.add_event, name="add_event"),
    path('edit_event', views.edit_event, name="edit_event"),
    path('save_edit', views.save_edit, name="save_edit"),
    path('user_settings', views.user_settings, name="user_settings"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('remove_image', views.remove_image, name="remove_image"),
    path('remove_event', views.remove_event, name="remove_event"),
    path('info', views.info, name="info"),
    path('rate', views.rate, name="rate"),
    path('edit_comment', views.edit_comment, name="edit_comment"),
    path('study_material_save', views.study_material_save, name="study_material_save"),
    path('study_mat', views.study_mat, name="study_mat"),
    path('add_user_to_event', views.add_user, name="add_user"),
    path('remove_comment', views.remove_comment, name="remove_comment"),
    path('', views.index, name="index"),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
