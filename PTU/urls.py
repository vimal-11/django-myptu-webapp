"""PTU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('feeds/', include('feeds.urls', namespace='feeds')),
    path('', include('authenticate.urls')),
    path('forum/', include('forums.urls')),
    path('friend/', include('friend.urls', namespace='friend')),
    path('tinymce/', include('tinymce.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('exam/', include('exams.urls')),

     # Password reset links 
     # https://github.com/django/django/blob/master/django/contrib/auth/views.py

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                    template_name='password_reset/password_change_done.html'), 
            name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
                    template_name='password_reset/password_change.html'), 
            name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                    template_name='password_reset/password_reset_done.html'),
            name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                    template_name='password_reset/password_change.html'), 
            name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
                    template_name='password_reset/password_reset_form.html'), 
            name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                    template_name='password_reset/password_reset_complete.html'),
            name='password_reset_complete'),
]



