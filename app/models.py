from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models
from django.db.models import Q, Avg
from django.contrib.auth import get_user_model

User = get_user_model()

class Studio(models.Model):
    name = models.CharField(
        max_length=125,
        verbose_name='Название студии'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=125,
        verbose_name='Название жанра'
    )

    def __str__(self):
        return self.name


class AnimeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(Q(status='В бане')|Q(status='Редактура'))


class Anime(models.Model):

    title_ru = models.CharField(
        max_length=125,
        verbose_name='название на русском'
    )
    slug = models.SlugField()
    title_en = models.CharField(
        max_length=125,
        verbose_name='название на английском'
    )
    title_jp = models.CharField(
        max_length=125,
        verbose_name='название на японском'
    )
    description = models.TextField(
        verbose_name='Описание аниме'
    )
    cover = models.ImageField(
        upload_to='media/covers/',
        verbose_name='Обложка аниме'
    )
    type = models.CharField(
        max_length=125,
        choices=(
            ('Tv', 'Tv serial'),
            ('Web', 'Web serial'),
            ('Streaming', 'Streaming serial')
        ),
        verbose_name='Тип аниме'
    )
    date_publish = models.DateField(
        verbose_name='Дата выхода аниме'
    )
    status = models.CharField(
        max_length=125,
        choices=(
            ('Скоро выйдет', 'Скоро выйдет'),
            ('Продолжается', 'Продолжается'),
            ('Завершен', 'Завершен'),
            ('Приостановлен', 'Приостановлен'),
            ('В бане', 'В бане'),
            ('Редактура', 'Редактура')
        )
    )
    # status = models.CharField(
    #     max_length=125,
    #     choices=(
    #         ('В планах', 'В планах'),
    #         ('Смотрю', 'Смотрю'),
    #         ('Забросил', 'Забросил'),
    #         ('Досмотрел', 'Досмотрел')
    #     )
    # )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Рейтинг аниме',
    )
    duration_per_episode = models.CharField(
        max_length=125,
        verbose_name='продолжительность на эпизод'
    )
    quality = models.CharField(
        max_length=125,
        choices=(
            ('360p', '360p'),
            ('480p', '480p'),
            ('HD', 'HD'),
            ('4K', '4K'),
            ('8K', '8K'),
        ),
        verbose_name='Разрешение видео'
    )
    count_of_views = models.PositiveIntegerField(
        verbose_name='Количество просмотров'
    )
    count_of_votes = models.PositiveIntegerField(
        verbose_name='Количество оценок'
    )
    count_of_comments = models.PositiveIntegerField(
        verbose_name='Количество комментариев'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    age_limit = models.PositiveSmallIntegerField(
        choices=(
            (3, 'pg-3'),
            (7, 'pg-7'),
            (12, 'pg-12'),
            (16, 'pg-16'),
            (18, 'pg-18'),
        ),
        verbose_name='Рейтинг PG'
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='genres'
    )
    studios = models.ManyToManyField(
        Studio,
        verbose_name='Студии',
        related_name='studios'
    )

    objects = AnimeManager()

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'


class Season(models.Model):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.PROTECT,
        verbose_name='Аниме',
        related_name='seasons'
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер сезона'
    )
    name = models.CharField(
        max_length=125,
        verbose_name='Название сезона'
    )
    total_episodes_count = models.PositiveSmallIntegerField(
        verbose_name='Общее количество серий которые планируются'
    )
    total_episodes_released_count = models.PositiveSmallIntegerField(
        verbose_name='Общее количество серий которые вышли'
    )
    date_publish = models.DateField(
        verbose_name='Дата выпуска сезона'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )

    def __str__(self):
        return f"{self.anime}  {self.name}"


class Episode(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        verbose_name='Сезон',
        related_name='episodes'
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер эпизода'
    )
    file = models.FileField(
        upload_to='media/files/'
    )
    name = models.CharField(
        max_length=125,
        verbose_name='Название эпизода'
    )
    file = models.FileField(
        upload_to='media/files/'
    )
    date_publish = models.DateField(
        verbose_name='Дата выпуска cерии'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    description = models.TextField(
        verbose_name='Описание эпизода'
    )
    cover = models.ImageField(
        upload_to='media/episode/covers/',
        verbose_name='обложка эпизода'
    )

    def __str__(self):
        return f'{self.season} {self.name}'

    def save(self, *args, **kwargs):
        self.season.total_episodes_released_count += 1
        self.season.save()

        super().save(*args, **kwargs)


class AnimeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name='comments'
                              )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    rating = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(limit_value=5),
            MinValueValidator(limit_value=1)
        )
    )
    body = models.TextField(verbose_name='Комментарий')

    def save(self, *args, **kwargs):

        anime_review_instance = super(AnimeReview, self).save(*args, **kwargs)

        self.anime.count_of_comments += 1
        self.anime.count_of_votes += 1
        self.anime.rating = round(Anime.objects.annotate(rate=Avg('comments__rating')).get(pk=self.anime.pk).rate, 1)
        self.anime.save()

        return anime_review_instance


class AnimeEpisodeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    body = models.TextField(verbose_name='Коментарий')


