from calendar import monthcalendar, month_name
from datetime import datetime, date, timedelta

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import KakeboMonth, KakeboWeek, KakeboWeekTable
from ..forms import SelectYearWeekFormSet, KakeboWeekForm
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

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
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
        context["income"], context["outflow"] = self.obj.display_totals_budget
        context["spare_cost"] = self.obj.spare_cost
        context["target_reach"] = self.obj.target_reach
        context["spare"] = "%.2f" % self.obj.spare
        available_money = self.obj.display_available_money
        context["available_money"] = "%.2f" % available_money if available_money else None

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
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
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
        return context

    @staticmethod
    def get_list_day(today: datetime) -> list:
        list_days = []
        for i in range(7):
            data__ = f"{today.strftime('%A')} - {today.strftime('%d')}"
            list_days.append(data__)
            today += timedelta(days=1)
        return list_days
