from django.contrib import admin

from .models import KakeboMonth, KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance


@admin.register(KakeboMonth)
class KakeboMonthAdmin(admin.ModelAdmin):
    """Kakebo month model admin."""

    autocomplete_fields = ["user"]


@admin.register(KakeboWeek)
class KakeboWeekAdmin(admin.ModelAdmin):
    """Kakebo week model admin."""

    autocomplete_fields = ["user"]


@admin.register(KakeboWeekTable)
class KakeboWeekTableAdmin(admin.ModelAdmin):
    """Kakebo week table model admin."""


@admin.register(KakeboEndOfMonthBalance)
class KakeboEndOfMonthBalanceAdmin(admin.ModelAdmin):
    """Kakebo end of month balance model admin."""
