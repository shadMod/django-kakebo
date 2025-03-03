from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..constants import ANSWER_SMILE_LIST
from ..models import KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance
from ..models.kakebo_week_table import KakeboCostColors
from ..utils import get_user_from_user_kakebo_composed

register = template.Library()


@register.filter(is_safe=True)
@register.simple_tag
def render_total_weeks(user_kakebo_composed: str, color: str) -> str:
    """Template tag to render total weeks.

    Args:
        user_kakebo_composed (str): Value composed of user_val, month, year in one word
            (e.g. 'username-month-year').
        color (str): Color string from KakeboCostColors.colors_costs.

    Returns:
        str: Return the render total week.
    """
    user, kakebo_month = get_user_from_user_kakebo_composed(user_kakebo_composed)
    kakebo_week_list = KakeboWeek.objects.filter(user=user, month=kakebo_month)
    type_cost = int(KakeboCostColors.colors_costs.index(color))
    total_table_values = [
        "%.2f"
        % KakeboWeekTable.objects.get(
            kakebo=kakebo_week, type_cost=type_cost
        ).display_total_table
        for kakebo_week in kakebo_week_list
    ]

    html = f"""
        <table class="w-100">
            <thead>
                <tr>
                    <th colspan="2">
                        <p class="bg-{color} py-2 ps-3 text-white">
                            {KakeboCostColors.constant_choices[type_cost]}
                        </p>
                    </th>
                </tr>
            </thead>
            <tbody>
    """

    for week_number, value in enumerate(total_table_values, 1):
        html += f"""
            <tr>
                <td class="bx-{color} px-15">
                    <p class="mb-2">
                        week {week_number}
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-{color} mb-2 text-end">
                        € {value}
                    </p>
                </td>
            </tr>
        """

    html += f"""
            <tr>
                <td class="bg-{color} bx-{color} px-15">
                    <p class="mt-2 mb-1 text-white">
    """
    html += _("total")
    html += f"""
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-{color} mb-2 text-end">
                        € {'%.2f' % sum(list(map(float, total_table_values)))}
                    </p>
                </td>
            </tr>
        </tbody>
    </table>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_cost_relevant(
    user_kakebo_composed: str, nr_cost: int, rows: int = 5, disabled: bool = False
) -> str:
    """Template tag to render cost relevant.

    Args:
        user_kakebo_composed (str): Value composed of user_val, month, year in one word
            (e.g. 'username-month-year').
        nr_cost (int): Number of cost.
        rows (int, optional): Number of rows. Defaults to 5.
        disabled (bool, optional): If True, disable input cost. Defaults to False.

    Returns:
        str: Return the render cost relevant.
    """
    disabled = "disabled" if disabled else ""
    user, kakebo_month = get_user_from_user_kakebo_composed(user_kakebo_composed)
    kakebo_end_of_month_balance = KakeboEndOfMonthBalance.objects.get(
        month=kakebo_month
    )
    cost_key, cost_data = kakebo_end_of_month_balance.get_costs_data()

    html = f"""
    <table class="w-100">
        <thead>
            <tr>
                <th>
                    <p class="bg-slategrey py-2 ps-3 text-white">
                        costo {nr_cost}
                    </p>
                </th>
                <th class="px-15">
                    <p class="bb-dashed-slategrey mb-2 text-end">
                        <input type="text" name="cost_{nr_cost}_name" id="id_cost_{nr_cost}_name" {disabled}
    """

    if cost_key:
        html += f"value='{cost_key}' class='text-end'>"
    else:
        html += ">"

    html += """
                    </p>
                </th>
            </tr>
        </thead>
        <tbody>
    """

    for row in range(1, rows + 1):
        value_cost_data = (
            f"value='{cost_data[f'cost_{row}']}' class='text-end'>"
            if cost_data
            else ">"
        )
        html += f"""
            <tr>
                <td class="bs-slategrey px-15">
                    <p class="mb-2">
                        week {row}
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-slategrey mb-2 text-end">
                        <input type="number" step="any" min="0"  placeholder="0.00"
                            name="cost_{nr_cost}_{row}" id="id_cost_{nr_cost}_{row}"
                            class="text-end text-basic-roow" {disabled} {value_cost_data}
                    </p>
                </td>
            </tr>
        """

    html += """
            <tr>
                <td class="bg-slategrey bx-slategrey px-15">
                    <p class="mt-2 mb-1 text-white">
    """
    html += _("total")
    html += f"""
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-slategrey mb-2 text-end">
                        € {"%.2f" % kakebo_end_of_month_balance.tot_costs(nr_cost, False)}
                    </p>
                </td>
            </tr>

        </tbody>
    </table>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_month_cost(user_kakebo_composed: str, rows: int = 5) -> str:
    """Template tag to render month cost.

    Args:
        user_kakebo_composed (str): Value composed of user_val, month, year in one word
            (e.g. 'username-month-year').
        rows (int, optional): Number of rows. Defaults to 5.

    Returns:
        str: Return the render cost relevant.
    """
    html = "<tbody>"
    list_row = rows + 1

    user, kakebo_month = get_user_from_user_kakebo_composed(user_kakebo_composed)
    kakebo_end_of_month_balance = KakeboEndOfMonthBalance.objects.get(
        month=kakebo_month
    )

    for nr_week, kakebo_week in enumerate(
        KakeboWeek.objects.filter(user=user, month=kakebo_month), 1
    ):
        total_table_list = [
            table.display_total_table
            for table in KakeboWeekTable.objects.filter(kakebo=kakebo_week)
        ]
        total_table = sum(list(map(float, total_table_list)))
        del total_table_list

        html += "<tr>"
        if nr_week == 1:
            html += f"""
                <td class="w-33 align-top text-end p-3" rowspan="{list_row + 1}">
                    <h5 class="text-lightseagreen">
            """
            html += _("weekly expenses")
            html += """
                    </h5>
                </td>
            """

        css_value = "bt-lightseagreen" if nr_week == 1 else ""
        html += f"""
                <td class="bg-lightseagreen {css_value} px-15">
                    <p class="mt-2 mb-1 text-white">
                        week {nr_week}
                    </p>
                </td>
                <td class="px-15 {css_value} bx-lightseagreen">
                    <p class="bb-dashed-lightseagreen mb-2 text-end">
                        {"%.2f" % total_table}
                    </p>
                </td>
        """
        html += "</tr>"

    html += """
        <tr>
            <td class="bg-lightseagreen bb-lightseagreen px-15">
                <p class="mt-2 mb-1 text-white">
    """
    html += _("utilities")
    html += f"""
                </p>
            </td>
            <td class="bb-lightseagreen bx-lightseagreen px-15">
                <p class="bb-dashed-lightseagreen mb-0 text-end">
                    € {kakebo_end_of_month_balance.display_total_utilities}
                </p>
            </td>
        </tr>
        </tbody>
        <tbody>
            <tr>
                <td>
                    <br>
                </td>
            </tr>
        </tbody>
        <tbody>
            <tr>
                <td></td>
                <td class="bg-lightseagreen px-15">
                    <p class="mt-2 mb-1 text-white">
    """
    html += _("total month cost")
    html += f"""
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-lightseagreen mb-2 text-end">
                        € {kakebo_end_of_month_balance.display_total_month}
                    </p>
                </td>
            </tr>
        </tbody>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_answer_smile(answer: str) -> str:
    """Template tag to render smile tag from answer.

    Args:
        answer (str): Answer from kakebo template form.

    Returns:
        str: Return the render cost smile tag from answer.
    """
    smile_tag = ANSWER_SMILE_LIST[answer]
    html = f"""
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#{smile_tag}Modal">
        <i class="bi bi-emoji-{smile_tag} h1"></i><br/>{answer}
    </button>
    
    <div class="modal fade" id="{smile_tag}Modal" tabindex="-1" aria-labelledby="{smile_tag}ModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>
                        Sei sicuro della tua decisione?
                    </p>
                    <p>
                        Cliccando invio chiuderai il mese e non sarà possibile effettuare
                        modifiche al mese corrente
                    </p>
                </div>
                <div class="modal-footer w-100">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-6">
                                <button type="button" class="btn btn-secondary w-100" data-dismiss="modal">
                                    Torna indietro
                                </button>
                            </div>
                            <div class="col-6">
                                <button type="submit" class="btn btn-primary w-100" name="answer_{answer}_check">
                                    Invia
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return mark_safe(html)
