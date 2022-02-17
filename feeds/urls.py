from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:user_id>/', views.OwnerPostsView.as_view(), name='my-posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_id>/comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('post/<int:post_id>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
