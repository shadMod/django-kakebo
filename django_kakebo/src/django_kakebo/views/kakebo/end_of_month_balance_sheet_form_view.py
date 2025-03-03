from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from ...constants import (
    NUMBER_OF_COSTS_IN_REPORT,
    DEFAULT_LIST_UTILITIES,
)
from ...forms import EndOfMonthBalanceSheetForm
from ...models import KakeboMonth, KakeboWeek, KakeboEndOfMonthBalance
from ...models.kakebo_week_table import KakeboCostColors
from ...utils import KeyKakebo


class EndOfMonthBalanceSheetFormView(LoginRequiredMixin, FormView, KeyKakebo):
    form_class = EndOfMonthBalanceSheetForm
    template_name = "basic/kakebo/month-balance.html"
    current_kakebo_report = None

    def dispatch(self, request: WSGIRequest, *args, **kwargs) -> TemplateResponse:
        """Dispatch the form view to Kakebo week form.

        Args:
            request (WSGIRequest): WSGI request.

        Returns:
            TemplateResponse: Template response.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user = self.request.user
        kakebo_month = KakeboMonth.objects.get(
            user=user,
            month=self.kwargs["month"],
            year=self.kwargs["year"],
        )
        self.kwargs["tot_available"] = kakebo_month.display_available_money
        kakebo_week = KakeboWeek.objects.filter(user=user, month=kakebo_month)
        self.kwargs["len_week"] = len(kakebo_week)

        self.current_kakebo_report, _ = KakeboEndOfMonthBalance.objects.get_or_create(
            month=kakebo_month
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: EndOfMonthBalanceSheetForm) -> HttpResponseRedirect:
        """Validate form to save EndOfMonthBalanceSheetForm record.

        Args:
            form (EndOfMonthBalanceSheetForm): Form to validate.

        Returns:
            HttpResponseRedirect: HTTP response redirect.
        """
        cd = form.cleaned_data

        if not self.current_kakebo_report.conclusion:
            fields_to_update = DEFAULT_LIST_UTILITIES + ["answer_1", "answer_2"]
            for field in fields_to_update:
                if field in ["answer_1", "answer_2"]:
                    value_to_update = cd.get(field, "")
                else:
                    value_to_update = cd.get(field) if cd.get(field) else 0
                setattr(self.current_kakebo_report, field, value_to_update)

            costs = {}
            for index_report_cost in range(NUMBER_OF_COSTS_IN_REPORT):
                key_name = cd.get(f"cost_{index_report_cost}_name")
                if key_name:
                    costs[key_name] = {
                        f"cost_{index}": cd.get(f"cost_{index_report_cost}_{index}", 0)
                        for index in range(1, 6)
                    }
            self.current_kakebo_report.costs_data = costs

            if "answer_yes_check" in self.request.POST:
                self.current_kakebo_report.conclusion = 1
            if "answer_almost_check" in self.request.POST:
                self.current_kakebo_report.conclusion = 2
            if "answer_no_check" in self.request.POST:
                self.current_kakebo_report.conclusion = 3

        self.current_kakebo_report.answer_3 = cd.get("answer_3", "")
        self.current_kakebo_report.save()
        return self.get_success_url()

    def get_success_url(self) -> HttpResponseRedirect:
        """Get the success url.

        Returns:
            HttpResponseRedirect: Return http response redirect to success url.
        """
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-balance",
                kwargs={
                    "year": self.kwargs["year"],
                    "month": self.kwargs["month"],
                },
            )
        )

    def get_initial(self, **kwargs) -> dict[str, Any]:
        """Return the initial data to use for forms on this view.

        Returns:
            Return the initial dict data to use for forms on this view.
        """
        return {
            "conclusion": self.current_kakebo_report.conclusion,
            "answer_1": self.current_kakebo_report.answer_1,
            "answer_2": self.current_kakebo_report.answer_2,
            "answer_3": self.current_kakebo_report.answer_3,
        }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context data.

        Returns:
            dict[str, Any]: Return context data.
        """
        context = super().get_context_data(**kwargs)
        context["list_django_kakebo_colors"] = KakeboCostColors.colors_costs
        context["key_kakebo"] = self.get_key_kakebo
        context["list_utilities"] = [
            (
                utility_field,
                getattr(self.current_kakebo_report, f"display_{utility_field}"),
            )
            for utility_field in DEFAULT_LIST_UTILITIES
        ]
        context["tot_utilities"] = self.current_kakebo_report.display_total_utilities
        context["tot_costs"] = self.current_kakebo_report.display_total_month
        context["diff_available_costs"] = (
            self.current_kakebo_report.display_diff_available_costs
        )
        context["obj_conclusion"] = self.current_kakebo_report.get_conclusion_display
        context["disabled"] = (
            "disabled" if self.current_kakebo_report.conclusion else ""
        )
        return {**context, **self.kwargs}
