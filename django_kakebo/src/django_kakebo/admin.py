from django.contrib import admin

from .models import KakeboWeek


@admin.register(KakeboWeek)
class KakeboWeekAdmin(admin.ModelAdmin):
    pass
