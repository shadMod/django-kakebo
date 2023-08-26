from django.contrib import admin

from .models import KakeboMonth, KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance


@admin.register(KakeboMonth)
class KakeboMonthAdmin(admin.ModelAdmin):
    pass


@admin.register(KakeboWeek)
class KakeboWeekAdmin(admin.ModelAdmin):
    search_fields = ['kakebo']
    autocomplete_fields = ['user']


@admin.register(KakeboWeekTable)
class KakeboWeekTableAdmin(admin.ModelAdmin):
    pass


@admin.register(KakeboEndOfMonthBalance)
class KakeboEndOfMonthBalanceAdmin(admin.ModelAdmin):
    pass
