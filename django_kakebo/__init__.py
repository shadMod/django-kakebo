import os

from .src.django_kakebo.apps import DjangoKakeboConfig

DIR_PACKAGE = os.path.dirname(os.path.realpath(__file__))

DIR_TEMPLATE = os.path.join(DIR_PACKAGE, "src", "themes")

DJANGO_KAKEBO_TEMPLATETAGS = {
    "render_balance": "django_kakebo.src.django_kakebo.templatetags.render_balance",
    "render_budget": "django_kakebo.src.django_kakebo.templatetags.render_budget",
    "render_kakebo": "django_kakebo.src.django_kakebo.templatetags.render_kakebo",
}

DIR_STATIC_KAKEBO = os.path.join(DIR_PACKAGE, "src", "django_kakebo", "static")
DIR_STATIC_USER = os.path.join(DIR_PACKAGE, "src", "user", "static")
