from datetime import datetime, date, timedelta
from logging import getLogger

from django.db import models
from django.conf import settings

from .constants import colors

User = settings.AUTH_USER_MODEL
logger = getLogger(__name__)


class KakeboMonth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(default=1)
    year = models.PositiveSmallIntegerField(default=1980)
    budget: dict = models.JSONField(default=dict)
    spare_cost = models.TextField(blank=True, null=True, default="")
    target_reach = models.TextField(blank=True, null=True, default="")
    spare = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        verbose_name_plural = "Kakebo Month"

    def __str__(self):
        return f"{self.user.username}'s Kakebo - {self.month}/{self.year}"

    @property
    def display_totals_budget(self) -> (float, float):
        income = "%.2f" % self.get_totals_budget[0]
        outflow = "%.2f" % self.get_totals_budget[1]
        return income, outflow

    @property
    def display_available_money(self):
        income, outflow = self.display_totals_budget
        if self.spare:
            return float(income) - float(outflow) - self.spare
        return None

    @property
    def get_totals_budget(self) -> (float, float):
        income = float(0)
        outflow = float(0)
        for key, val in self.budget.items():
            if "_income_" in key:
                value = val.get("value_income") if val.get("value_income") else 0
                income += float(value)
            if "_outflow_" in key:
                value = val.get("value_outflow") if val.get("value_outflow") else 0
                outflow += float(value)
        return income, outflow


class KakeboWeek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.ForeignKey(KakeboMonth, on_delete=models.CASCADE)
    week = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Kakebo Week"

    def __str__(self):
        start = self.display_start_week
        end = self.display_end_week
        return f"{self.user.username}'s Kakebo - {start} // {end}"

    @property
    def display_start_week(self) -> date:
        date_w = f"{self.month.year}-{self.week}-1"
        return datetime.strptime(date_w, "%Y-%W-%w").date()

    @property
    def display_end_week(self) -> date:
        return self.display_start_week + timedelta(days=6)

    @property
    def total_week(self):
        return sum([obj.display_total_table for obj in KakeboWeekTable.objects.filter(kakebo=self)])


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


class KakeboEndOfMonthBalance(models.Model):
    month = models.ForeignKey(KakeboMonth, on_delete=models.CASCADE)
    electricity = models.FloatField(default=0)
    gas = models.FloatField(default=0)
    tel_internet = models.FloatField(default=0)
    water = models.FloatField(default=0)
    waste = models.FloatField(default=0)
    costs_data: dict = models.JSONField(default=dict)
    answer_1 = models.TextField(blank=True, null=True, default="")
    answer_2 = models.TextField(blank=True, null=True, default="")
    answer_3 = models.TextField(blank=True, null=True, default="")

    LIST_TYPE = [
        (0, ""),
        (1, "yes"),
        (2, "almost"),
        (3, "no"),
    ]
    conclusion: int = models.PositiveSmallIntegerField(
        choices=LIST_TYPE, default=0,
    )

    @property
    def display_electricity(self):
        return "%.2f" % self.electricity

    @property
    def display_gas(self):
        return "%.2f" % self.gas

    @property
    def display_tel_internet(self):
        return "%.2f" % self.tel_internet

    @property
    def display_water(self):
        return "%.2f" % self.water

    @property
    def display_waste(self):
        return "%.2f" % self.waste

    @property
    def display_total_utilities(self):
        return "%.2f" % self.total_utilities

    @property
    def total_utilities(self):
        attrs = ["electricity", "gas", "tel_internet", "water", "waste"]
        return sum([getattr(self, x) for x in attrs])

    @property
    def display_diff_available_costs(self):
        return "%.2f" % self.diff_available_costs

    @property
    def display_total_month(self):
        return "%.2f" % self.total_month

    @property
    def total_month(self):
        val = sum([x.total_week for x in KakeboWeek.objects.filter(month=self.month)])
        val += self.total_utilities
        return val

    @property
    def diff_available_costs(self):
        return self.month.display_available_money - self.total_month

    def get_key_list(self):
        """
        get a list of all key in costs_data
        """
        return list(self.costs_data.keys())

    def get_key_cost(self, nr_key: int = 0) -> str:
        key_list = self.get_key_list()
        if nr_key <= len(key_list) - 1:
            key = key_list[nr_key]
        else:
            key = ""
        return key

    def tot_costs(self, nr_key: int, counter0: bool = True) -> float:
        """
        :counter0:  True if the counter starts from zero, if not put it false
        """
        if not counter0:
            nr_key -= 1
        key = self.get_key_cost(nr_key)
        val = 0
        if key:
            val = sum([x for x in self.costs_data[key].values() if x])
        return val


# settings models
class UtilitiesCost(models.Model):
    name = models.CharField(max_length=150)
