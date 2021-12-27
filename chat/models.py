from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import related


class Rooms(models.Model):
    room = models.CharField(null=True, max_length=30, default='test')
    user_created = models.ForeignKey(User, related_name='room_author', on_delete=models.CASCADE, null=True)
    channel_name = models.TextField(null=True)

    def __str__(self):
        return self.room

class Message(models.Model):
    author = models.ForeignKey(User, related_name='message_author', on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, null=True, on_delete=models.CASCADE)
    msg_content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_20_messages():
        return Message.objects.order_by('-time').all()[:20]

