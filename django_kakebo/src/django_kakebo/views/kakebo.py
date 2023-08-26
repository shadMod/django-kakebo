from calendar import monthcalendar, month_name
from datetime import datetime, date, timedelta

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import KakeboMonth, KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance
from ..forms import SelectYearWeekFormSet, KakeboWeekForm, EndOfMonthBalanceSheetForm
from ..constants import colors
from ..utils import find_indices


class Index(TemplateView):
    template_name = "basic/home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["five_reason"] = [
            {
                "name": "ORDINE",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-list-ul"></i>',
            },
            {
                "name": "CONTROLLO",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-controller"></i>',
            },
            {
                "name": "RISPARMIO",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-piggy-bank"></i>',
            },
            {
                "name": "AUTODISCIPLINA",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-cup-hot"></i>',
            },
            {
                "name": "SERENITA'",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-emoji-laughing"></i>',
            },
        ]
        return context


class SelectYearWeekFormView(LoginRequiredMixin, FormView):
    form_class = SelectYearWeekFormSet
    template_name = "basic/kakebo/calendar.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # set month and year in kwargs if they aren't exist
        if not self.kwargs.get("month"):
            self.kwargs["month"] = date.today().month
        if not self.kwargs.get("year"):
            self.kwargs["year"] = date.today().year

        # init obj in self
        self.obj, _ = KakeboMonth.objects.get_or_create(
            user=self.request.user,
            month=self.kwargs['month'],
            year=self.kwargs['year'],
        )

        obj_reports = KakeboEndOfMonthBalance.objects.filter(month=self.obj)
        if obj_reports:
            self.obj_report = obj_reports[0]
            self.conclusion = self.obj_report.conclusion
        else:
            self.obj_report, self.conclusion = None, None

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.obj_report.conclusion:
            budget = {}
            for i, row in enumerate(form.cleaned_data):
                budget[f'_income_{i}'] = {}
                budget[f'_outflow_{i}'] = {}
                for key, value in row.items():
                    if '_income' in key:
                        if isinstance(value, (datetime, date)):
                            value = value.strftime("%Y-%m-%d")
                        value = "" if value is None else value
                        budget[f'_income_{i}'][key] = value
                    if '_outflow' in key and value:
                        if isinstance(value, (datetime, date)):
                            value = value.strftime("%Y-%m-%d")
                        budget[f'_outflow_{i}'][key] = value
            self.obj.budget = budget

            cd_0 = form.cleaned_data[0]
            if cd_0:
                self.obj.spare_cost = cd_0.get("spare_cost", "")
                self.obj.target_reach = cd_0.get("target_reach", "")
                self.obj.spare = cd_0.get("spare") if cd_0.get("spare") else 0

            self.obj.save()
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-calendar", kwargs={
                    "year": self.kwargs["year"],
                    "month": self.kwargs["month"],
                },
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month, year = self.kwargs['month'], self.kwargs['year']

        context["day_list"] = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        context["week_list"] = self.get_week_dict(
            monthcalendar(year, month)
        )

        context["month"] = f"{month_name[month]} {year}"
        context['key_kakebo'] = f'{self.request.user.username}-{self.kwargs["month"]} - {self.kwargs["year"]}'
        context["income"], context["outflow"] = self.obj.display_totals_budget
        context["spare_cost"] = self.obj.spare_cost
        context["target_reach"] = self.obj.target_reach
        context["spare"] = "%.2f" % self.obj.spare
        available_money = self.obj.display_available_money
        context["available_money"] = "%.2f" % available_money if available_money else None
        context['disabled'] = "disabled" if self.conclusion else ""
        return context

    def get_week_dict(self, week_list) -> dict:
        nr_week = self.get_nr_week(week_list)
        for week in week_list:
            for i, day in enumerate(week):
                week[i] = ("", day)

        # set first week
        week = week_list[0]
        if ("", 0) in week:
            day = 31
            month = self.kwargs['month'] - 1
            for i in sorted(find_indices(week, ("", 0)), reverse=True):
                week[i] = ("another-month", day, month)
                day -= 1

        # set last week
        week = week_list[-1]
        if ("", 0) in week:
            day = 1
            month = self.kwargs['month'] + 1
            for i in find_indices(week, ("", 0)):
                week[i] = ("another-month", day, month)
                day += 1

        week_dict = {}
        for i, week in enumerate(week_list):
            week_dict[nr_week[i]] = week

        return week_dict

    def get_nr_week(self, week_list):
        nr_week = []
        for week in week_list:
            day = [x for x in week if x][0]
            nr_week.append(date(self.kwargs['year'], self.kwargs['month'], day).isocalendar().week)
        return nr_week


class KakeboWeekFormView(LoginRequiredMixin, FormView):
    form_class = KakeboWeekForm
    template_name = "basic/kakebo/week.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # init year and week in self
        self.year = kwargs['year']
        self.week = kwargs['week']

        # get month by year and week
        date_w = f"{self.year}-{self.week}-1"
        month = datetime.strptime(date_w, "%Y-%W-%w").month
        # get KakeboMonth()
        self.obj_month, _ = KakeboMonth.objects.get_or_create(
            user=self.request.user,
            month=month,
            year=self.kwargs['year'],
        )

        # init obj with relative tables (=> tb_{color}) in self
        self.obj, _ = KakeboWeek.objects.get_or_create(
            user=self.request.user,
            month=self.obj_month,
            week=self.week,
        )
        for i, color in enumerate(colors):
            table, _ = KakeboWeekTable.objects.get_or_create(
                kakebo=self.obj, type_cost=i
            )
            setattr(self, f'tb_{color}', table)

        # init date from week and year param in self.time_
        self.time_ = self.obj.display_start_week

        obj_reports = KakeboEndOfMonthBalance.objects.filter(month=self.obj_month)
        if obj_reports:
            self.obj_report = obj_reports[0]
            self.conclusion = self.obj_report.conclusion
        else:
            self.obj_report, self.conclusion = None, None

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.conclusion is not None:
            cd = form.cleaned_data
            for color in colors:
                data = {}
                for clm, day in enumerate(self.get_list_day(self.time_)):
                    data[clm] = {}
                    for row in range(9):
                        tag_name = f"tag_name_{color}_{clm}_{row}"
                        desc = cd.get(f"{tag_name}_desc", None)
                        value = cd.get(f"{tag_name}_value", None)
                        if desc or value:
                            data[clm][row] = {"desc": desc, "value": value}
                obj = getattr(self, f'tb_{color}')
                obj.data_row = data
                obj.save()
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-week", kwargs={
                    "year": self.kwargs["year"],
                    "week": self.kwargs["week"],
                },
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_tr = []
        list_type = KakeboWeekTable.LIST_TYPE
        # TODO: add management in back-office view
        for i, lenrows in enumerate([10, 7, 7, 7]):
            list_tr.append((colors[i], lenrows, list_type[i][1]))
        context['list_tr'] = list_tr

        context['cell_'] = self.get_list_day(self.time_)
        context['row_'] = [i for i in range(7)]
        context['key_kakebo'] = f'{self.request.user.username}-{self.kwargs["year"]}-{self.kwargs["week"]}'

        totals_days = []
        for i in range(7):
            totals = []
            for color in colors:
                obj = getattr(self, f'tb_{color}')
                totals.append(obj.total_column(i))
            totals_days.append('%.2f' % (sum(totals)))

        context["totals_days"] = totals_days
        context["total_week"] = sum(list(map(float, totals_days)))
        context['disabled'] = "disabled" if self.conclusion else ""
        return context

    @staticmethod
    def get_list_day(today: datetime) -> list:
        list_days = []
        for i in range(7):
            data__ = f"{today.strftime('%A')} - {today.strftime('%d')}"
            list_days.append(data__)
            today += timedelta(days=1)
        return list_days


class EndOfMonthBalanceSheetFormView(LoginRequiredMixin, FormView):
    form_class = EndOfMonthBalanceSheetForm
    template_name = "basic/kakebo/month-balance.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user = self.request.user
        self.obj_month = KakeboMonth.objects.get(
            user=user,
            month=self.kwargs["month"],
            year=self.kwargs["year"],
        )
        self.obj_list = KakeboWeek.objects.filter(user=user, month=self.obj_month)
        self.obj, _ = KakeboEndOfMonthBalance.objects.get_or_create(
            month=self.obj_month
        )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data

        if not self.obj.conclusion:
            self.obj.electricity = cd['electricity'] if cd['electricity'] else 0
            self.obj.gas = cd['gas'] if cd['gas'] else 0
            self.obj.tel_internet = cd['tel_internet'] if cd['tel_internet'] else 0
            self.obj.water = cd['water'] if cd['water'] else 0
            self.obj.waste = cd['waste'] if cd['waste'] else 0
            self.obj.answer_1 = cd['answer_1']
            self.obj.answer_2 = cd['answer_2']

            costs = {}
            for j in range(2):
                key_name = cd[f"cost_{j}_name"]
                if key_name:
                    costs[key_name] = {}
                    for i in range(1, 6):
                        costs[key_name][f"cost_{i}"] = cd[f"cost_{j}_{i}"]
            self.obj.costs_data = costs

            # save KakeboEndOfMonthBalance()
            self.obj.save()

            if "answer_yes_check" in self.request.POST:
                self.obj.conclusion = 1
            if "answer_almost_check" in self.request.POST:
                self.obj.conclusion = 2
            if "answer_no_check" in self.request.POST:
                self.obj.conclusion = 3
            self.obj.save()

        self.obj.answer_3 = cd['answer_3']
        self.obj.save()

        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-balance", kwargs={
                    "year": self.kwargs["year"],
                    "month": self.kwargs["month"],
                },
            )
        )

    def get_initial(self, **kwargs):
        initial = {
            "conclusion": self.obj.conclusion,
            "answer_1": self.obj.answer_1,
            "answer_2": self.obj.answer_2,
            "answer_3": self.obj.answer_3,
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_colors'] = colors
        context['key_kakebo'] = f'{self.request.user.username}-{self.kwargs["year"]}-{self.kwargs["month"]}'
        list_utilities = ["electricity", "gas", "tel_internet", "water", "waste"]
        context['list_utilities'] = [(x, getattr(self.obj, f"display_{x}")) for x in list_utilities]
        context['tot_utilities'] = self.obj.display_total_utilities
        context['len_week'] = len(self.obj_list)
        context['tot_available'] = self.obj_month.display_available_money
        context['tot_costs'] = self.obj.display_total_month
        context['diff_available_costs'] = self.obj.display_diff_available_costs
        context['obj_conclusion'] = self.obj.get_conclusion_display
        context['disabled'] = "disabled" if self.obj.conclusion else ""
        return context
