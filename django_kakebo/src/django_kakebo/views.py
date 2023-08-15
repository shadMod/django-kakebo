from datetime import datetime, timedelta

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView

from .models import KakeboWeek
from .forms import KakeboWeekForm
from .constants import colors


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

        self.obj, _ = KakeboWeek.objects.get_or_create(
            # user=self.kwargs["username"],
            year=self.kwargs["year"],
            week=self.kwargs["week"],
        )
        self.year = kwargs['year']
        self.week = kwargs['week']
        self.time_ = self.get_time
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data

        data = {}
        for j in range(4):
            data[j] = {}
            color = colors[j]
            for clm, day in enumerate(self.get_list_day(self.time_)):
                data[j][clm] = {}
                for i in range(9):
                    tag_name = f"tag_name_{color}_{clm}_{i}"
                    desc = cd.get(f"{tag_name}_desc", None)
                    value = cd.get(f"{tag_name}_value", None)
                    if desc or value:
                        data[j][clm][i] = {"desc": desc, "value": value}

        self.obj.data_row = data
        self.obj.save()
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(
            reverse_lazy(
                "kakebo-week", kwargs={
                    "username": self.kwargs["username"],
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
        context['key_kakebo'] = f'{self.kwargs["username"]}-{self.kwargs["year"]}-{self.kwargs["week"]}'
        return context

    @property
    def get_time(self) -> datetime:
        date_w = f"{self.year}-{self.week}-1"
        return datetime.strptime(date_w, "%Y-%W-%w")

    @staticmethod
    def get_list_day(today: datetime) -> list:
        list_days = []
        for i in range(7):
            data__ = f"{today.strftime('%A')} - {today.strftime('%d')}"
            list_days.append(data__)
            today += timedelta(days=1)
        return list_days
