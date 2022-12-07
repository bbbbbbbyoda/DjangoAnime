from django.contrib import admin

from .models import Studio, Genre, Anime, Season, Episode, AnimeReview, AnimeEpisodeReview

class AnimeAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "type",)
    prepopulated_fields = {'slug': ('title_ru', )}

admin.site.register(Studio)
admin.site.register(Genre)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(AnimeReview)
admin.site.register(AnimeEpisodeReview)
