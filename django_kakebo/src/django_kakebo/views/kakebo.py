from datetime import datetime, timedelta

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView

from ..models import KakeboWeek, KakeboWeekTable
from ..forms import KakeboWeekForm
from ..constants import colors


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


class KakeboWeekFormView(FormView):
    form_class = KakeboWeekForm
    template_name = "basic/kakebo/week.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            pass

        # init year and week in self
        self.year = kwargs['year']
        self.week = kwargs['week']

        # init obj with relative tables (=> tb_{color}) in self
        self.obj, _ = KakeboWeek.objects.get_or_create(
            user=self.request.user,
            year=self.year,
            week=self.week,
        )
        for i, color in enumerate(colors):
            table, _ = KakeboWeekTable.objects.get_or_create(
                kakebo=self.obj, type_cost=i
            )
            setattr(self, f'tb_{color}', table)

        # init date from week and year param in self.time_
        self.time_ = self.obj.display_start_week
        return super().dispatch(*args, **kwargs)

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
        for i, lenrows in enumerate([9, 7, 7, 7]):
            list_tr.append((colors[i], lenrows))
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
