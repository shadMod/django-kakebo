from django.contrib import admin

from .models import KakeboWeek, KakeboWeekTable


@admin.register(KakeboWeek)
class KakeboWeekAdmin(admin.ModelAdmin):
    pass


@admin.register(KakeboWeekTable)
class KakeboWeekTableAdmin(admin.ModelAdmin):
    pass
