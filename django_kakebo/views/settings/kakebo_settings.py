from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class KakeboSettings(LoginRequiredMixin, TemplateView):
    """Kakebo setting view."""

    template_name = "settings/settings.html"
