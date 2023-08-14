from datetime import datetime, timedelta

from django.views.generic import TemplateView


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


class KakeboWeek(TemplateView):
    template_name = "basic/kakebo/week.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cell_'] = self.get_list_day("07082023")
        context['row_'] = [i for i in range(7)]
        return context

    def get_list_day(self, today: str = None) -> list:
        if today is None:
            today = datetime.now()
        else:
            today = datetime.strptime(today, "%d%m%Y")

        list_days = []
        for i in range(7):
            data__ = f"{today.strftime('%A')} - {today.strftime('%d')}"
            list_days.append(data__)
            today += timedelta(days=1)

        return list_days
