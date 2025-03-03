from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class KakeboThemes(LoginRequiredMixin, TemplateView):
    """Kakebo theme view."""

    template_name = "settings/themes.html"
