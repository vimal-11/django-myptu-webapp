# Generated by Django 3.2.6 on 2021-09-03 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_rename_pyqs_pyq'),
    ]

    operations = [
        migrations.CreateModel(
            name='PYQs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.CharField(max_length=300)),
                ('year', models.IntegerField(null=True)),
                ('year_slug', models.SlugField(max_length=4)),
                ('category', models.CharField(blank=True, max_length=300, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('link', models.URLField(unique=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('exam_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam_detail')),
            ],
        ),
        migrations.DeleteModel(
            name='PYQ',
        ),
    ]
