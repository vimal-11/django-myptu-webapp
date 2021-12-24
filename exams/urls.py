from django.contrib import admin
from django.urls import path
from . import views

app_name = 'exams'
urlpatterns = [
    #path('update/', views.examupdate, name="examupdate"),
    path('<slug>/', views.exam, name="exam"),
    path("<slug:exam_slug>/<slug:field_slug>/", views.exam_detail, name="exam_detail"),
    path("<slug:exam_slug>/<slug:field_slug>/<slug:year_slug>/", views.pyqs, name="pyqs"),  
]
