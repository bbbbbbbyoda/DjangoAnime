from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from .models import Anime, Season, Episode, AnimeReview, AnimeEpisodeReview, Genre


def index(request):

    all_anime = Anime.objects.all()

    context = {
        'trending_now': all_anime,
        'popular_shows': all_anime,
        'recently_added_shows': all_anime
    }


    return render(request, template_name='app/index.html', context=context)


def anime_detail(request, slug):

    anime = Anime.objects.get(slug=slug)
    comments = AnimeReview.objects.filter(anime=anime)

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect('login')

        body = request.POST.get('body')
        star = request.POST.get('star')

        AnimeReview(user=request.user, anime=anime, body=body, rating=star).save()

    return render(request, template_name='app/anime-detail.html',
                  context={'anime': anime, 'comments': comments})


def anime_episodes(request, slug):

    anime = Anime.objects.get(slug=slug)

    return render(request, template_name='app/anime-episodes.html', context={'anime': anime})


def anime_watch(request, slug, season_number, episode_number):

    anime = Anime.objects.get(slug=slug)
    season = Season.objects.get(anime=anime, number=season_number)
    episode = Episode.objects.get(season=season, number=episode_number)
    comments = AnimeEpisodeReview.objects.filter(episode=episode)

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect('login')

        body = request.POST.get('body')
        AnimeEpisodeReview(user=request.user, episode=episode, body=body).save()

    context = {
        'anime': anime,
        'episode': episode,
        'slug': slug,
        'comments': comments
    }

    prev_season = Season.objects.filter(anime=anime, number=season_number - 1).first()
    next_season = Season.objects.filter(anime=anime, number=season_number + 1).first()

    if episode_number != 1 and not prev_season:
        context['prev_episode'] = {'episode': episode_number - 1, 'season': season_number}
    elif prev_season and episode_number == 1:
        context['prev_season'] = {'episode': prev_season.total_episodes_count, 'season': season_number - 1}
    elif episode_number != 1 and season_number != season.total_episodes_count:
        context['prev_episode'] = {'episode': episode_number - 1, 'season': season_number}

    if season.total_episodes_count == episode_number and next_season:
        context['next_season'] = {'episode': 1, 'season': season_number + 1}
    elif season.total_episodes_released_count != episode_number:
        context['next_episode'] = {'episode': episode_number + 1, 'season': season_number}

    return render(request, template_name='app/anime-watching.html', context=context)


def anime_categories(request):
    genres = Genre.objects.all()
    all_anime = Anime.objects.all()

    if request.method == "GET":

        genre = request.GET.get('genre')
        anime_genres = Anime.objects.filter(genres__name=genre)

        p = Paginator(anime_genres, 1)  # creating a paginator object
        # getting the desired page number from url
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

    return render(request, template_name='app/categories.html', context={'genres': genres,
                                                                         'all_anime': all_anime,
                                                                         'anime_genres': anime_genres,
                                                                         'page_obj': page_obj,
                                                                         "genre": genre})

