from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class KakeboDashboardSetting(LoginRequiredMixin, TemplateView):
    template_name = "settings/dashboard.html"


class KakeboSettings(LoginRequiredMixin, TemplateView):
    template_name = "settings/settings.html"


class KakeboThemes(LoginRequiredMixin, TemplateView):
    template_name = "settings/themes.html"
