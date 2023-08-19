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
    data_row: dict = models.JSONField(default=dict)

    LIST_TYPE = [
        (0, "basic necessities"),
        (1, "optional"),
        (2, "culture and leisure"),
        (3, "extras and unexpected"),
    ]
    type_cost: int = models.PositiveSmallIntegerField(
        choices=LIST_TYPE,
        default=0,
    )

    @property
    def display_type_cost_color(self) -> str:
        return colors[self.type_cost]

    @property
    def display_total_table(self) -> float:
        return sum([self.total_column(i) for i in range(len(self.data_row))])

    @property
    def list_sort_cost(self) -> list:
        data = []
        for row in self.data_row.values():
            data.extend([v for v in row.values()])
        sort_ = sorted([x for x in data], key=lambda x: x['value'], reverse=True)
        return sort_

    def get_column(self, clm: int) -> list:
        clm = self.data_row.get(f'{clm}', {})
        if clm:
            return [(x.get('desc', ""), x.get('value', 0)) for x in clm.values()]
        return []

    def get_cell(self, clm: int, row: int) -> tuple:
        return self.get_column(clm)[row]

    def get_list_sort_cost(self, max_row: int) -> list:
        max_row -= 1
        list_cost = self.list_sort_cost[:max_row]

        if list_cost:
            other_cost = 0
            for i in self.list_sort_cost[max_row:]:
                other_cost += i["value"]
            if len(list_cost) >= max_row:
                list_cost.append({"desc": "others", "value": other_cost})
        return list_cost

    def total_column(self, clm: int) -> float:
        clm = self.get_column(clm)
        if clm:
            return sum([x[1] for x in clm])
        return float(0)
