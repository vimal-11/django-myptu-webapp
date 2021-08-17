from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'forums'
urlpatterns = [
    path('', views.forum, name="forum"),
    path('topic/<slug>/', views.topic, name="topic"),
    path('query/<slug>/', views.query, name="query"),
    path('new_query/', views.newquery, name="newquery"),
    path('search', views.search_results, name="search_results"),

]