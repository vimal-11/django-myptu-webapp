from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Category, Query, Reply

# Register your models here.

admin.site.register(Category)
admin.site.register(Query)
admin.site.register(Reply)