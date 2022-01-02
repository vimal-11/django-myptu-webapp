from django.db import models
from django.db.models.base import Model
from django.db.models.fields import related
from django.conf import settings


class Rooms(models.Model):
    room = models.CharField(null=True, max_length=30, default='test')
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='room_author', on_delete=models.CASCADE, null=True)
    channel_name = models.TextField(null=True)

    def __str__(self):
        return self.room

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_author', on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    msg_content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_20_messages():
        return Message.objects.order_by('-time').all()[:20]

