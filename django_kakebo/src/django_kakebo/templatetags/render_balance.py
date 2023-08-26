from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ..constants import colors as list_colors, name_type_cost
from ..models import KakeboMonth, KakeboWeek, KakeboWeekTable, KakeboEndOfMonthBalance

register = template.Library()


@register.filter(is_safe=True)
@register.simple_tag
def render_total_weeks(kakebo: str, color: str):
    username, year, month = kakebo.split('-')
    # get User()
    user = User.objects.get(username=username)
    # get KakeboMonth()
    obj_month = KakeboMonth.objects.get(
        user=user,
        month=month,
        year=year,
    )
    obj_list = KakeboWeek.objects.filter(user=user, month=obj_month)
    type_cost = int(list_colors.index(color))
    data = []
    for obj in obj_list:
        val = KakeboWeekTable.objects.get(kakebo=obj, type_cost=type_cost).display_total_table
        data.append("%.2f" % val)

    html = f"""
        <table class="w-100">
            <thead>
                <tr>
                    <th colspan="2">
                        <p class="bg-{color} py-2 ps-3 text-white">
                            {name_type_cost[type_cost]}
                        </p>
                    </th>
                </tr>
            </thead>
            <tbody>
    """

    for i, val in enumerate(data, 1):
        html += f"""
            <tr>
                <td class="bx-{color} px-15">
                    <p class="mb-2">
                        week {i}
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-{color} mb-2 text-end">
                        € {val}
                    </p>
                </td>
            </tr>
        """

    total = "%.2f" % sum(list(map(float, data)))
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
                        € {total}
                    </p>
                </td>
            </tr>
        """

    html += """
        </tbody>
    </table>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_cost_relevant(kakebo: str, nr_cost: int, row: int = 5, disabled: bool = False):
    disabled = "disabled" if disabled else ""
    username, year, month = kakebo.split('-')
    # get User()
    user = User.objects.get(username=username)
    # get KakeboMonth()
    obj_month = KakeboMonth.objects.get(
        user=user,
        month=month,
        year=year,
    )
    obj = KakeboEndOfMonthBalance.objects.get(month=obj_month)
    costs = obj.costs_data

    key, data = "", {}
    if costs:
        key_list = list(costs.keys())
        if len(key_list) >= nr_cost:
            key = key_list[nr_cost - 1]
            data = costs[key]

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

    if key:
        html += f"value='{key}' class='text-end'>"
    else:
        html += f">"

    html += f"""
                    </p>
                </th>
            </tr>
        </thead>
        <tbody>
    """

    for i in range(1, row + 1):
        html += f"""
            <tr>
                <td class="bs-slategrey px-15">
                    <p class="mb-2">
                        week {i}
                    </p>
                </td>
                <td class="px-15">
                    <p class="bb-dashed-slategrey mb-2 text-end">
                        <input type="number" step="any" min="0"  placeholder="0.00"
                            name="cost_{nr_cost}_{i}" id="id_cost_{nr_cost}_{i}"
                            class="text-end text-basic-roow" {disabled}
        """
        if data:
            html += f"value='{data[f'cost_{i}']}' class='text-end'>"
        else:
            html += f">"
        """
                    </p>
                </td>
            </tr>
        """

    html += f"""
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
                        € {"%.2f" % obj.tot_costs(nr_cost, False)}
                    </p>
                </td>
            </tr>

        </tbody>
    </table>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_month_cost(kakebo: str, row: int = 5):
    html = "<tbody>"
    list_row = row + 1
    username, year, month = kakebo.split('-')
    # get User()
    user = User.objects.get(username=username)
    # get KakeboMonth()
    obj_month = KakeboMonth.objects.get(
        user=user,
        month=month,
        year=year,
    )
    obj_endmonth = KakeboEndOfMonthBalance.objects.get(month=obj_month)

    for i, obj in enumerate(KakeboWeek.objects.filter(user=user, month=obj_month), 1):
        data = []
        for table in KakeboWeekTable.objects.filter(kakebo=obj):
            data.append(table.display_total_table)
        val = sum(list(map(float, data)))

        html += "<tr>"
        if i == 1:
            html += f"""
                <td class="w-33 align-top text-end p-3" rowspan="{list_row + 1}">
                    <h5 class="text-lightseagreen">
                        spese settimali
                    </h5>
                </td>
            """

        css_value = ""
        if i == 1:
            css_value = "bt-lightseagreen"

        html += f"""
                <td class="bg-lightseagreen {css_value} px-15">
                    <p class="mt-2 mb-1 text-white">
                        week {i}
                    </p>
                </td>
                <td class="px-15 {css_value} bx-lightseagreen">
                    <p class="bb-dashed-lightseagreen mb-2 text-end">
                        {"%.2f" % val}
                    </p>
                </td>
        """
        html += "</tr>"

    obj = KakeboEndOfMonthBalance.objects.get(month=obj_month)
    html += f"""
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
                    € {obj.display_total_utilities}
                </p>
            </td>
        </tr>
    """

    # white space
    html += """
        </tbody>
        <tbody>
            <tr>
                <td>
                    <br>
                </td>
            </tr>
        </tbody>
    """

    html += """
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
                        € {obj_endmonth.display_total_month}
                    </p>
                </td>
            </tr>
        </tbody>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_answer_smile(answer: int):
    answer_list = [
        ("yes", "sunglasses"),
        ("almost", "expressionless"),
        ("no", "frown"),
    ]
    answer = answer_list[answer]

    html = f"""
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#{answer[1]}Modal">
        <i class="bi bi-emoji-{answer[1]} h1"></i><br/>{answer[0]}
    </button>
    
    <div class="modal fade" id="{answer[1]}Modal" tabindex="-1" aria-labelledby="{answer[1]}ModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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
                                <button type="submit" class="btn btn-primary w-100" name="answer_{answer[0]}_check">
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
