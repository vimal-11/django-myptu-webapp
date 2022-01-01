from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

from friend.models import FriendList

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
			    email=self.normalize_email(email),
			    username=username,
		)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "myptu/default_profile_image.png"



class Account(AbstractBaseUser):
    
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    first_name 			    = models.CharField(max_length=30,default='')
    last_name               = models.CharField(max_length=30,default='')
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email				= models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username
    
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=Account)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)   

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
    

