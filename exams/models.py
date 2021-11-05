from re import T
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.shortcuts import reverse

class Exam(models.Model):
    exam = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.exam
    
    def get_url(self):
        return reverse("exams:exam", kwargs={
            "slug": self.slug
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.exam)
        super(Exam, self).save(*args, **kwargs)

        

class Exam_Detail(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, null=True)
    field = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    reg_link = models.URLField(blank=True)
    syllabus = HTMLField(blank=True)
    important_dates = HTMLField(blank=True)

    def __str__(self):
        return self.field

    def get_url(self):
        return reverse("exams:exam_detail", kwargs={
            "exam_slug": self.exam.slug,
            "field_slug": self.slug,
        })


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.field)
        super(Exam_Detail, self).save(*args, **kwargs)



class Pyqs(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    exam_field = models.ForeignKey('Exam_Detail', on_delete=models.CASCADE)
    phase = models.CharField(max_length=300, blank=True, null=True)
    year = models.IntegerField(null=True)
    year_slug = models.SlugField(max_length=4)
    category = models.CharField(max_length=300, blank=True, null=True)
    subject = models.CharField(max_length=100)
    question_link = models.URLField()
    answer_link = models.URLField(blank=True, null=True)

    def get_url(self):
        return reverse("exams:pyqs", kwargs={
            "exam_slug": self.exam.slug,
            "field_slug": self.exam_field.slug,
            "year_slug": self.year_slug
        })

    def save(self, *args, **kwargs):
        if not self.year_slug:
            self.year_slug = slugify(self.year)
        super(Pyqs, self).save(*args, **kwargs)

    def __str__(self):
        if self.phase is not None:
            return self.phase
        else:
            return self.subject
    
class Gate_Syllabus(models.Model):
    year = models.IntegerField(null=True)
    gate_paper = models.CharField(max_length=100)
    syllabus = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.gate_paper