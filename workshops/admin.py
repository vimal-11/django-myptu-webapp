from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Workshop, Registered_workshop
# Register your models here.
admin.site.register(Workshop)
admin.site.register(Registered_workshop)
