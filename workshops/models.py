from django.conf import Settings
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings

# Create your models here.
class Workshop(models.Model):
    workshop_title = models.CharField(max_length = 100)
    description=models.TextField()
    category = models.CharField(max_length = 100)
    date = models.TextField()
    price = models.TextField()

    def __str__(self):
        return self.workshop_title

class Registered_workshop(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'registered_user',on_delete = models.CASCADE,null = True)
    workshop_id = models.ForeignKey(Workshop,on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    expiry = models.BooleanField()

