from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authenticate'
urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/signup', views.signup, name="signup"),
    path('accounts/logout', views.logoutUser, name="logout"),
    path('accounts/login', views.loginUser, name="login"),
    path('index', views.index, name="index"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('profile/<int:pk>', views.profile_view.as_view(), name="profilepage"),
    path('search/', views.account_search_view, name="search"),
    #path('signup', views.MakeCreate.as_view(), name='signup'),
]
