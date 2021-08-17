from django import forms
from django.db.models import fields
from django.forms import models
from .models import Query

class NewQuery(forms.ModelForm):
    class Meta:
        model = Query
        fields = ["title", "content", "categories", "tags"]