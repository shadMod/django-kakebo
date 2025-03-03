from django.db import models

from .kakebo_month import KakeboMonth
from .kakebo_week import KakeboWeek
from ..constants import DEFAULT_LIST_UTILITIES


class KakeboEndOfMonthBalance(models.Model):
    """Kakebo end of month balance model."""

    month = models.ForeignKey(KakeboMonth, on_delete=models.CASCADE)
    electricity = models.FloatField(default=0)
    gas = models.FloatField(default=0)
    tel_internet = models.FloatField(default=0)
    water = models.FloatField(default=0)
    waste = models.FloatField(default=0)
    costs_data = models.JSONField(default=dict)
    answer_1 = models.TextField(blank=True, default="")
    answer_2 = models.TextField(blank=True, default="")
    answer_3 = models.TextField(blank=True, default="")

    LIST_TYPE = [
        (0, ""),
        (1, "yes"),
        (2, "almost"),
        (3, "no"),
    ]
    conclusion: int = models.PositiveSmallIntegerField(choices=LIST_TYPE, default=0)

    @property
    def display_electricity(self) -> str:
        """Display the electricity amount of the kakebo end of month.

        Returns:
            str: The electricity amount of the kakebo end of month as string.
        """
        return "%.2f" % self.electricity

    @property
    def display_gas(self) -> str:
        """Display the gas amount of the kakebo end of month.

        Returns:
            str: The gas amount of the kakebo end of month as string.
        """
        return "%.2f" % self.gas

    @property
    def display_tel_internet(self) -> str:
        """Display the internet and telephone amount of the kakebo end of month.

        Returns:
            str: The internet and telephone amount of the kakebo end of month as string.
        """
        return "%.2f" % self.tel_internet

    @property
    def display_water(self) -> str:
        """Display the water amount of the kakebo end of month.

        Returns:
            str: The water amount of the kakebo end of month as string.
        """
        return "%.2f" % self.water

    @property
    def display_waste(self) -> str:
        """Display the waste amount of the kakebo end of month.

        Returns:
            str: The waste amount of the kakebo end of month as string.
        """
        return "%.2f" % self.waste

    @property
    def display_total_utilities(self) -> str:
        """Display the total utilities of the kakebo end of month.

        Returns:
            str: The total utilities of the kakebo end of month as string.
        """
        return "%.2f" % self.total_utilities

    @property
    def total_utilities(self) -> float:
        """Total utilities of the kakebo end of month.

        Returns:
            float: The total utilities of the kakebo end of month.
        """
        return sum(
            [getattr(self, utility_field) for utility_field in DEFAULT_LIST_UTILITIES]
        )

    @property
    def display_diff_available_costs(self) -> str:
        """Display the difference available costs of the kakebo end of month.

        Returns:
            str: The difference available costs of the kakebo end of month as string.
        """
        return "%.2f" % self.diff_available_costs

    @property
    def display_total_month(self) -> str:
        """Display the total month of the kakebo end of month.

        Returns:
            str: The total month of the kakebo end of month as string.
        """
        return "%.2f" % self.total_month

    @property
    def total_month(self) -> float:
        """Total month of the kakebo end of month.

        Returns:
            float: The total month of the kakebo end of month.
        """
        return (
            sum(
                [
                    kakebo_week.sum_total_week
                    for kakebo_week in KakeboWeek.objects.filter(month=self.month)
                ]
            )
            + self.total_utilities
        )

    @property
    def diff_available_costs(self) -> float:
        """Display the difference available costs of the kakebo end of month.

        Returns:
            float: The difference available costs of the kakebo end of month.
        """
        return self.month.display_available_money - self.total_month

    def get_key_cost(self, key_index: int = 0) -> str:
        """Get key cost from number of key.


        Args:
            key_index (int, optional): The index of the key. Defaults to 0.

        Returns:
            str: The key cost from number of key.
        """
        key_list = list(self.costs_data.keys())
        return key_list[key_index] if key_index <= len(key_list) - 1 else ""

    def tot_costs(self, key_index: int, counter_0: bool = True) -> float:
        """Total costs of the kakebo end of month.

        Args:
            key_index (int): The index of the key.
            counter_0 (): True if the counter starts from zero, False otherwise.

        Returns:
            float: The total costs of the kakebo end of month.
        """
        if not counter_0:
            key_index -= 1
        key = self.get_key_cost(key_index)
        return sum([x for x in self.costs_data[key].values() if x]) if key else 0

    def get_costs_data(self, nr_cost: int = 1) -> dict:
        key_list = self.costs_data.keys()
        if len(key_list) >= nr_cost:
            cost_key = key_list[nr_cost - 1]
            cost_data = self.costs_data[cost_key]
            return cost_key, cost_data
        return "", {}
