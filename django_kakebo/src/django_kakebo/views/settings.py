from django.views.generic import TemplateView


class KakeboDashboardSetting(TemplateView):
    template_name = "settings/dashboard.html"


class KakeboSettings(TemplateView):
    template_name = "settings/settings.html"


class KakeboThemes(TemplateView):
    template_name = "settings/themes.html"
