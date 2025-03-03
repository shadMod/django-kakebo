from datetime import datetime, timedelta
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView

from ...constants import (
    DEFAULT_ROWS_WEEK_FORM,
    NUMBER_OF_DAYS_IN_WEEK,
)
from ...forms import KakeboWeekForm
from ...models import KakeboMonth, KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance
from ...models.kakebo_week_table import KakeboCostColors
from ...services.kakebo_week_service import KakeboWeekService
from ...utils import KeyKakebo


class KakeboWeekFormView(LoginRequiredMixin, FormView, KeyKakebo):
    """Kakebo week form view."""

    form_class = KakeboWeekForm
    template_name = "basic/kakebo/week.html"
    field_list = ["username", "year", "week"]
    _service = KakeboWeekService()

    def __init__(self, **kwargs) -> None:
        """Initialize form view."""
        super().__init__(**kwargs)
        self.year = now().year
        self.conclusion = None

    def dispatch(self, request: WSGIRequest, *args, **kwargs) -> TemplateResponse:
        """Dispatch the form view to Kakebo week form.

        Args:
            request (WSGIRequest): WSGI request.

        Returns:
            TemplateResponse: Template response.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.year = kwargs.get("year", self.year)
        current_week = kwargs["week"] - 1

        self.kwargs["week_previous"] = self._service.get_previous_year_week(
            self.year, current_week
        )
        self.kwargs["week_next"] = self._service.get_next_year_week(
            self.year, current_week
        )

        year_week = f"{self.year}-{current_week}-1"
        month = datetime.strptime(year_week, "%Y-%W-%w").month
        self.kwargs["month"] = month
        self.kwargs["date"] = datetime.strptime(year_week, "%Y-%W-%w").date()

        kakebo_month, _ = KakeboMonth.objects.get_or_create(
            user=self.request.user, month=month, year=self.year
        )
        kakebo_week, _ = KakeboWeek.objects.get_or_create(
            user=self.request.user, month=kakebo_month, week=current_week
        )

        for index, color in enumerate(KakeboCostColors.colors_costs):
            kakebo_week_table, _ = KakeboWeekTable.objects.get_or_create(
                kakebo=kakebo_week, type_cost=index
            )
            setattr(self, f"tb_{color}", kakebo_week_table)

        kakebo_end_record = KakeboEndOfMonthBalance.objects.filter(
            month=kakebo_month
        ).first()
        self.conclusion = kakebo_end_record.conclusion if kakebo_end_record else None
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: KakeboWeekForm) -> HttpResponseRedirect:
        """Validate form and save all kakebo week table records.

        Args:
            form (KakeboWeekForm): kakebo week form.

        Returns:
            HttpResponseRedirect: HTTP response redirect.
        """
        if self.conclusion is None:
            cd = form.cleaned_data
            for color in KakeboCostColors.colors_costs:
                data = {}
                for column, day in enumerate(self.get_list_day()):
                    data[column] = {}
                    for row in range(9):
                        tag_name = f"tag_name_{color}_{column}_{row}"
                        desc = cd.get(f"{tag_name}_desc", None)
                        value = cd.get(f"{tag_name}_value", None)
                        if desc or value:
                            data[column][row] = {"desc": desc, "value": value}
                kakebo_week_table = getattr(self, f"tb_{color}")
                kakebo_week_table.data_row = data
                kakebo_week_table.save()
        return self.get_success_url()

    def get_success_url(self) -> HttpResponseRedirect:
        """Get the success url.

        Returns:
            HttpResponseRedirect: Return http response redirect to success url.
        """
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-week",
                kwargs={
                    "year": self.kwargs["year"],
                    "week": self.kwargs["week"],
                },
            )
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context data.

        Returns:
            dict[str, Any]: Return context data.
        """
        context = super().get_context_data(**kwargs)
        context["list_tr"] = [
            (type_cost, len_rows)
            for type_cost, len_rows in zip(
                KakeboCostColors.type_list, DEFAULT_ROWS_WEEK_FORM
            )
        ]

        context["cell_"] = self.get_list_day()
        context["key_kakebo"] = self.get_key_kakebo

        totals_days = []
        for day in range(NUMBER_OF_DAYS_IN_WEEK):
            totals = []
            for color in KakeboCostColors.colors_costs:
                kakebo_week_table = getattr(self, f"tb_{color}")
                totals.append(kakebo_week_table.total_column(day))
            totals_days.append("%.2f" % (sum(totals)))

        context["totals_days"] = totals_days
        context["disabled"] = "disabled" if self.conclusion else ""
        return {**context, **self.kwargs}

    def get_list_day(self) -> list[str]:
        """Get list of days.

        Returns:
            list[str]: List of days.
        """
        today = self.kwargs["date"]
        list_days = []
        for i in range(7):
            list_days.append(f"{today.strftime('%A')} - {today.strftime('%d')}")
            today += timedelta(days=1)
        return list_days
