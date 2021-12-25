from django.urls import path

from . import views

app_name = 'friend'

urlpatterns = [
	
    path('friend_request/', views.send_friend_request, name='friend-request'),
    
]