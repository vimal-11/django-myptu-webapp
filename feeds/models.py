from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)

class Feeds(models.Model):
    author           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='post_author')
    body             = RichTextField(blank=True)
    slug             = models.SlugField(max_length=400, unique=True, blank=True)
    posted_on        = models.DateTimeField(default=timezone.now)
    likes            = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    hide_post        = models.BooleanField(default=False)
    # image            = models.ManyToManyField('Image', blank=True)
    image            = models.ImageField(_("Image"), upload_to=upload_to, default='posts/default.jpg')
    hitcount_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name = 'hitcount_generic_relation')
    tags             = TaggableManager(blank=True)

    def __str__(self):
        return str(self.author)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.author) + "-" + self.body[3:13])
        super(Feeds, self).save(*args, **kwargs)


class Comments(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    comment         = models.TextField()
    created_on      = models.DateTimeField(default=timezone.now)
    post            = models.ForeignKey('Feeds', on_delete=models.CASCADE)
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')
    parent          = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comments.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return self.comment


# class Image(models.Model):
# 	image           = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

# class Image(models.Model):
# 	video = models(upload_to='uploads/post_photos', blank=True, null=True)