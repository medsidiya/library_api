# Generated by Django 5.0.5 on 2025-02-11 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_remove_author_role_author_about_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='about',
        ),
        migrations.RemoveField(
            model_name='author',
            name='average_rating',
        ),
        migrations.RemoveField(
            model_name='author',
            name='fans_count',
        ),
        migrations.RemoveField(
            model_name='author',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='author',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='author',
            name='ratings_count',
        ),
        migrations.RemoveField(
            model_name='author',
            name='text_reviews_count',
        ),
        migrations.AddField(
            model_name='author',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
