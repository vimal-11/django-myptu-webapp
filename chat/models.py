from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import related

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='message_author', on_delete=models.CASCADE)
    msg_content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_20_messages():
        return Message.objects.order_by('-time').all()[:20]
        