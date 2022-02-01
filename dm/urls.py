from django.urls import path
from . import views

app_name = 'dm'

urlpatterns = [
	path('', views.private_chat_room_view, name='private-chat-room'),
	path('create_or_return_private_chat/', views.create_or_return_private_chat, name='create-or-return-private-chat'),
]