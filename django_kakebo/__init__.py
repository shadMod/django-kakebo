import os

from .apps import DjangoKakeboConfig

DIR_PACKAGE = os.path.dirname(os.path.realpath(__file__))

DIR_TEMPLATE = os.path.join(DIR_PACKAGE, "src", "themes")

DJANGO_KAKEBO_TEMPLATETAGS = {
    "render_balance": "django_kakebo.templatetags.render_balance",
    "render_budget": "django_kakebo.templatetags.render_budget",
    "render_kakebo": "django_kakebo.templatetags.render_kakebo",
}

DIR_STATIC_KAKEBO = os.path.join(DIR_PACKAGE, "django_kakebo", "static")
DIR_STATIC_USER = os.path.join(DIR_PACKAGE, "django_kakebo_user", "static")
