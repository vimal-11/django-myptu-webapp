from django.contrib import admin
from django.urls import URLPattern, path
from . import views
app_name = 'workshops'

urlpatterns = [
    #path('<slug>/', views.CategoryView, name = 'category'),
    path('',views.ListView)
    #path('<slug:workshop_slug>/',views.WorkshopView, name = 'workshops')

]