from django.contrib import admin
from django.urls import path
from . import views
app_name = 'workshops'

urlpatterns = [
    #path('<slug>/', views.CategoryView, name = 'category'),
    path('',views.ListView)
    path('<slug>/',views.WorkshopView,name="workshop")

]