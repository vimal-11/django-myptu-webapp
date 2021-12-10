# Generated by Django 3.2.6 on 2021-09-02 17:26

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(blank=True, max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('reg_link', models.URLField(blank=True, unique=True)),
                ('syllabus', tinymce.models.HTMLField()),
                ('important_dates', tinymce.models.HTMLField()),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
            ],
        ),
    ]
