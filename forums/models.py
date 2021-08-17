from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse

# Create your models here.

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self) :
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("forums:topic", kwargs={
            "slug": self.slug
        })

    @property
    def num_queries(self):
        return Query.objects.filter(categories = self).count()

    @property
    def last_query(self):
        return Query.objects.filter(categories = self).latest("date")


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'replies'
    
    def __str__(self) :
        return self.reply[:150]


class Query(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = HTMLField()
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
            related_query_name = 'hit_count_generic_relation'
    )
    tags = TaggableManager()
    replies = models.ManyToManyField(Reply, blank=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Query, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("forums:query", kwargs={
            "slug": self.slug
        })

    @property
    def num_rply(self):
        return self.replies.count()