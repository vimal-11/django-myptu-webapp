from django.conf import Settings
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify

# Create your models here.
class Workshop(models.Model):
    workshop_title = models.CharField(max_length = 100)
    description=models.TextField()
    slug = models.SlugField(max_length=50,unique=True,blank=True)
    category = models.CharField(max_length = 100)
    date = models.TextField()
    price = models.TextField()

    def __str__(self):
        return self.workshop_title
    def get_url(self):
        return reverse("workshop:workshop_title", kwargs={
            "slug" : self.slug
        })
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.workshop_title)
        super(Workshop, self).save(*args, **kwargs)

class Registered_workshop(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'registered_user',on_delete = models.CASCADE,null = True)
    workshop_id = models.ForeignKey(Workshop,on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    expiry = models.BooleanField()

