from django.db import models
from django import forms



# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=20,default='')
    first_name = models.CharField(max_length=30,default='')
    last_name = models.CharField(max_length=30,default='')
    email = models.EmailField(default='')
    date_of_birth = models.DateField(default='')
    contact_number = models.IntegerField()
    program_choices = [('BTECH', 'BTech.'), ('MTECH', 'Mtech'), ('MBA', 'MBA'), 
    ('PhD', 'PhD'), ('RESEARCH', 'Research')]
    program = models.CharField(choices=program_choices, default='BTECH', max_length=40)
    department = models.CharField(max_length=40,default='')
    section = models.IntegerField()
    create_password = models.CharField(max_length=30,default=' ')
    confirm_password = models.CharField(max_length=30,default=' ')
    YEAR_IN_SCHOOL_CHOICES = [
        ('FRESHMAN', 'Freshman'),
        ('SOPHOMORE', 'Sophomore'),
        ('JUNIOR', 'Junior'),
        ('SENIOR', 'Senior'),
        ('GRADUATE', 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=20,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default='FRESHMAN',)
    

