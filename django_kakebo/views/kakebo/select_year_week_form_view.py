from calendar import monthcalendar, monthrange, month_name
from datetime import datetime, date
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from ...constants import NAMES_OF_THE_DAYS
from ...forms import SelectYearWeekFormSet
from ...models import KakeboMonth, KakeboEndOfMonthBalance
from ...utils import find_indices, KeyKakebo


class SelectYearWeekFormView(LoginRequiredMixin, FormView, KeyKakebo):
    """View to display the grid week from specific year."""

    form_class = SelectYearWeekFormSet
    template_name = "basic/kakebo/calendar.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kakebo_month = None
        self.conclusion = None

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        """Dispatch method to display the grid week from specific year.

        Returns:
            HttpResponse: HTTP response.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.kwargs.get("month"):
            self.kwargs["month"] = date.today().month
        if not self.kwargs.get("year"):
            self.kwargs["year"] = date.today().year

        self.kakebo_month, _ = KakeboMonth.objects.get_or_create(
            user=self.request.user, month=self.kwargs["month"], year=self.kwargs["year"]
        )

        kakebo_end_of_month_balance = KakeboEndOfMonthBalance.objects.filter(
            month=self.kakebo_month
        ).first()
        self.conclusion = (
            kakebo_end_of_month_balance.conclusion
            if kakebo_end_of_month_balance
            else None
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SelectYearWeekFormSet) -> HttpResponseRedirect:
        """Validate form and update kakebo end month balance.

        Args:
            form (SelectYearWeekFormSet): SelectYearWeekForm set.

        Returns:
            HttpResponseRedirect: HTTP response redirect.
        """
        if not self.conclusion:
            budget = {}
            for row_numer, row in enumerate(form.cleaned_data):
                budget[f"_income_{row_numer}"] = {}
                budget[f"_outflow_{row_numer}"] = {}
                for key, value in row.items():
                    if "_income" in key:
                        if isinstance(value, (datetime, date)):
                            value = value.strftime("%Y-%m-%d")
                        value = "" if value is None else value
                        budget[f"_income_{row_numer}"][key] = value
                    if "_outflow" in key and value:
                        if isinstance(value, (datetime, date)):
                            value = value.strftime("%Y-%m-%d")
                        budget[f"_outflow_{row_numer}"][key] = value
            self.kakebo_month.budget = budget

            row_0 = form.cleaned_data[0]
            if row_0:
                self.kakebo_month.spare_cost = row_0.get("spare_cost", "")
                self.kakebo_month.target_reach = row_0.get("target_reach", "")
                self.kakebo_month.spare = (
                    row_0.get("spare") if row_0.get("spare") else 0
                )

            self.kakebo_month.save()
        return self.get_success_url()

    def get_success_url(self) -> HttpResponseRedirect:
        """Get the success url.

        Returns:
            HttpResponseRedirect: Return http response redirect to success url.
        """
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-calendar",
                kwargs={"year": self.kwargs["year"], "month": self.kwargs["month"]},
            )
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context data.

        Returns:
            dict[str, Any]: Return context data with all key and related values
                to create the month grid.
        """
        context = super().get_context_data(**kwargs)
        month, year = self.kwargs["month"], self.kwargs["year"]
        context["day_list"] = NAMES_OF_THE_DAYS
        context["week_list"] = self.get_week_dict(monthcalendar(year, month))
        context["month"] = f"{month_name[month]} {year}"
        context["key_kakebo"] = self.get_key_kakebo
        context["income"] = self.kakebo_month.display_total_income_budget
        context["outflow"] = self.kakebo_month.display_total_outflow_budget
        context["spare_cost"] = self.kakebo_month.spare_cost
        context["target_reach"] = self.kakebo_month.target_reach
        context["spare"] = "%.2f" % self.kakebo_month.spare
        available_money = self.kakebo_month.display_available_money
        context["available_money"] = (
            "%.2f" % available_money if available_money else None
        )
        context["disabled"] = "disabled" if self.conclusion else ""
        return context

    def get_week_dict(self, week_list: list[list[int]]) -> dict[int, list[int]]:
        """Get week dict from week list.

        Args:
            week_list (list[list[int]]): Matrix formed by lists containing
                the list of days in each week.

        Returns:
            dict[int, list[int]]: Return a dictionary in which each key corresponds
                to the number of weeks in the year with relative week corresponding
                to a list of arguments to be exploited to create the month grid.
        """
        nr_week = self.get_nr_week(week_list)
        week_list = list(map(lambda row: [("", val) for val in row], week_list))

        num_days = 1
        week = week_list[-1]
        if ("", 0) in week:
            if self.kwargs["month"] == 12:
                year, month = self.kwargs["year"] + 1, 1
            else:
                year, month = self.kwargs["year"], self.kwargs["month"] + 1
            for index in find_indices(week, ("", 0)):
                week[index] = ("another-month", num_days, month)
                num_days += 1

        week = week_list[0]
        if ("", 0) in week:
            if self.kwargs["month"] == 1:
                year, month = self.kwargs["year"] - 1, 12
            else:
                year, month = self.kwargs["year"], self.kwargs["month"] - 1
            _, num_days = monthrange(year, month)
            for index in sorted(find_indices(week, ("", 0)), reverse=True):
                week[index] = ("another-month", num_days, month)
                num_days -= 1

        return {
            nr_week[index_week_list]: week
            for index_week_list, week in enumerate(week_list)
        }

    def get_nr_week(self, week_list: list[list[int]]) -> list[int]:
        """Get number of week form a matrix with all days in a month.

        Args:
            week_list (list[list[int]]): Matrix formed by lists containing
                the list of days in each week.

        Returns:
            list[int]: Number of week form.
        """
        days = [next(filter(lambda x: x != 0, row)) for row in week_list]
        return [
            date(self.kwargs["year"], self.kwargs["month"], day).isocalendar().week
            for day in days
        ]
