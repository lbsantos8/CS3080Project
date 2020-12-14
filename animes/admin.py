from django.contrib import admin

from .models import Anime
# Register your models here.

class AnimeAdmin(admin.ModelAdmin):
	list_display = ("name",)


admin.site.register(Anime, AnimeAdmin)
