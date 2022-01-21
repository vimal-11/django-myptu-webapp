from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'feeds'

urlpatterns = [
    #path('',views.index, name="feeds"),
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
    #path('newpost/', views.NewPost.as_view(), name='create-post')
]

urlpatterns = format_suffix_patterns(urlpatterns)
