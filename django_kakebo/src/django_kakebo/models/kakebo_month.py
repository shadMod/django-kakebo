from typing import Any

from django.conf import settings
from django.db import models

from ..constants import CashFlowType

User = settings.AUTH_USER_MODEL


class KakeboMonth(models.Model):
    """Kakebo month model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(default=1)
    year = models.PositiveSmallIntegerField(default=1980)
    budget: dict[str, Any] = models.JSONField(default=dict)
    spare_cost = models.TextField(blank=True, null=True, default="")
    target_reach = models.TextField(blank=True, null=True, default="")
    spare = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        verbose_name_plural = "Kakebo Month"

    def __str__(self) -> str:
        """Return string representation of Kakebo month.

        Returns:
            str: String representation of Kakebo month.
        """
        return f"{self.user.username}'s Kakebo - {self.month}/{self.year}"

    def get_income_budget(self) -> list[float]:
        """Get all income from budget.

        Returns:
            list[float]: List of all income float from budget.
        """
        return self.get_value_from_budget(CashFlowType.income.value)

    def get_outflow_budget(self) -> list[float]:
        """Get all outflow from budget.

        Returns:
            list[float]: List of all outflow float from budget.
        """
        return self.get_value_from_budget(CashFlowType.outflow.value)

    @property
    def total_income_budget(self) -> int | float:
        """Get total income from budget.

        Returns:
            int | float: Return the total of incomes from budget.
        """
        return sum(self.get_income_budget())

    @property
    def total_outflow_budget(self) -> int | float:
        """Get total outflow from budget.

        Returns:
            int | float: Return the total of outflows from budget.
        """
        return sum(self.get_outflow_budget())

    @property
    def display_total_income_budget(self) -> str:
        """Display total income from budget.

        Returns:
            str: Return the total incomes from budget as a string.
        """
        return "%.2f" % self.total_income_budget

    @property
    def display_total_outflow_budget(self) -> str:
        """Display total outflow from budget.

        Returns:
            str: Return the total outflows from budget as a string.
        """
        return "%.2f" % self.total_outflow_budget

    @property
    def display_available_money(self) -> int | float:
        """Displays the available money for this month.

        Returns:
            int | float: Available money for this month.
        """
        return (
            float(self.display_total_income_budget)
            - float(self.display_total_outflow_budget)
            - self.spare
            if self.spare
            else 0
        )

    def get_value_from_budget(self, cash_flow_type: str) -> list[Any]:
        if cash_flow_type not in CashFlowType:
            raise ValueError("Invalid cash flow type.")
        return [
            float(val.get(f"value_{cash_flow_type}"))
            if val.get(f"value_{cash_flow_type}")
            else 0
            for key, val in self.budget.items()
            if f"_{cash_flow_type}_" in key
        ]
