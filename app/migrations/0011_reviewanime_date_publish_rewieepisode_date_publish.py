# Generated by Django 4.1.1 on 2022-09-23 08:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rewieepisode_reviewanime'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewanime',
            name='date_publish',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rewieepisode',
            name='date_publish',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
    ]