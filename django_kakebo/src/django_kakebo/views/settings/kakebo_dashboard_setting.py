from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class KakeboDashboardSetting(LoginRequiredMixin, TemplateView):
    """Kakebo dashboard setting view."""

    template_name = "settings/dashboard.html"
