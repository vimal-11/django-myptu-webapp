from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Exam, Exam_Detail, Pyqs

# Register your models here.

admin.site.register(Exam)
admin.site.register(Exam_Detail)
admin.site.register(Pyqs)


