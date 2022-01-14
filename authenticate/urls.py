from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authenticate'
urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logoutUser, name="logout"),
    path('login', views.loginUser, name="login"),
    path('index', views.index, name="index"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('profile/<int:pk>', views.profile_view.as_view(), name="profilepage"),
    path('search/', views.account_search_view, name="search"),
    path('profile/<user_id>/edit/info', views.edit_account_view, name="edit_account")
    #path('signup', views.MakeCreate.as_view(), name='signup'),
]
