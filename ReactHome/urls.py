from django.urls import path
from . import views

app_name = 'ReactHome'

urlpatterns = [
    #path('',views.index, name="feeds"),
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
]