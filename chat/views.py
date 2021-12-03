from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Rooms




def index(request):
    context = {}
    rooms = Rooms.objects.all()
    context['rooms'] = rooms
    return render(request, 'chat/index.html', context)

@login_required
def room(request, room_name):
    room = Rooms.objects.filter(room = room_name).first()
    chats = []
    if room:
        chats = Message.objects.filter(room = room)
    else:
        room = Rooms(room = room_name)
        room.save()
        
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chats': chats,
        #'username': request.user.username
    })