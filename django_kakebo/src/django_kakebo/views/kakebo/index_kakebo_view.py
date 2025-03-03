from typing import Any

from django.views.generic import TemplateView


class IndexKakeboView(TemplateView):
    template_name = "basic/home/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context data.

        Returns:
            dict[str, Any]: Return context data.
        """
        context = super().get_context_data(**kwargs)
        context["five_reason"] = [
            {
                "name": "ORDER",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-list-ul"></i>',
            },
            {
                "name": "CONTROL",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-controller"></i>',
            },
            {
                "name": "SAVINGS",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-piggy-bank"></i>',
            },
            {
                "name": "SELF-DISCIPLINE",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-cup-hot"></i>',
            },
            {
                "name": "SERENITY",
                "description": "Lorem ipsium",
                "favicon": '<i class="bi bi-emoji-laughing"></i>',
            },
        ]
        return context
