from django.contrib import admin

from .models import KakeboMonth, KakeboWeek, KakeboWeekTable


@admin.register(KakeboMonth)
class KakeboMonthAdmin(admin.ModelAdmin):
    pass


@admin.register(KakeboWeek)
class KakeboWeekAdmin(admin.ModelAdmin):
    pass


@admin.register(KakeboWeekTable)
class KakeboWeekTableAdmin(admin.ModelAdmin):
    pass
