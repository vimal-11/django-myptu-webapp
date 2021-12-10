# Generated by Django 3.2.6 on 2021-08-06 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0006_auto_20210806_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='confirm_password',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
        migrations.AddField(
            model_name='users',
            name='password1',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AddField(
            model_name='users',
            name='password2',
            field=models.CharField(default=' ', max_length=30),
        ),
    ]