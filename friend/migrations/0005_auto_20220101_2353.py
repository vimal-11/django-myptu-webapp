# Generated by Django 3.2.6 on 2022-01-01 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0004_alter_friendlist_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='sender',
        ),
        migrations.DeleteModel(
            name='FriendList',
        ),
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
