from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anime-detail/<slug:slug>/', views.anime_detail, name='anime_detail'),
    path('anime-episodes/<slug:slug>/', views.anime_episodes, name='anime_episodes'),
    path('anime-watching/<slug:slug>/season-<int:season_number>/episode-<int:episode_number>/', views.anime_watch, name='anime-watch'),
    path('anime_categories/', views.anime_categories, name='anime_categories'),
]
