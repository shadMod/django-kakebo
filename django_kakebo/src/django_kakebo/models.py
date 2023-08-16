from datetime import datetime, date, timedelta
from logging import getLogger

from django.db import models
from django.conf import settings

from .constants import colors

User = settings.AUTH_USER_MODEL
logger = getLogger(__name__)


class KakeboWeek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField(default=1)
    year = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Kakebo Week"

    def __str__(self):
        start = self.display_start_week
        end = self.display_end_week
        return f"{self.user.username}'s Kakebo - {start} // {end}"

    @property
    def display_start_week(self) -> date:
        date_w = f"{self.year}-{self.week}-1"
        return datetime.strptime(date_w, "%Y-%W-%w").date()

    @property
    def display_end_week(self) -> date:
        return self.display_start_week + timedelta(days=6)


class KakeboWeekTable(models.Model):
    kakebo = models.ForeignKey(KakeboWeek, on_delete=models.CASCADE)
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

    def get_column(self, clm: int) -> list:
        clm = self.data_row.get(f'{clm}', {})
        if clm:
            return [(x.get('desc', ""), x.get('value', 0)) for x in clm.values()]
        return []

    def get_cell(self, clm: int, row: int) -> tuple:
        return self.get_column(clm)[row]

    def total_column(self, clm: int) -> float:
        clm = self.get_column(clm)
        if clm:
            return sum([x[1] for x in clm])
        return float(0)
