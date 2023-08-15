from logging import getLogger

from django.db import models
from django.conf import settings

from .constants import colors

User = settings.AUTH_USER_MODEL
log = getLogger(__name__)


class KakeboWeek(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField(default=1)
    year = models.IntegerField(default=1)
    data_row = models.JSONField(default=dict)

    LIST_TYPE = [
        (0, "basic necessities"),
        (1, "optional"),
        (2, "culture and leisure"),
        (3, "extras and unexpected"),
    ]
    type_cost = models.PositiveSmallIntegerField(
        choices=LIST_TYPE,
        default=0,
    )

    def display_type_cost_color(self) -> str:
        return colors[self.type_cost]
