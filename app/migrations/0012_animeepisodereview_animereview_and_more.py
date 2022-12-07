# Generated by Django 4.1.1 on 2022-09-23 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0011_reviewanime_date_publish_rewieepisode_date_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimeEpisodeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('body', models.TextField(verbose_name='Коментарий')),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.episode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('body', models.TextField(verbose_name='Комментарий')),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.anime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='rewieepisode',
            name='episode',
        ),
        migrations.DeleteModel(
            name='ReviewAnime',
        ),
        migrations.DeleteModel(
            name='RewieEpisode',
        ),
    ]