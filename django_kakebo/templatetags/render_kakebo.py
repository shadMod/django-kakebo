from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..constants import NUMBER_OF_DAYS_IN_WEEK
from ..models import KakeboWeek, KakeboWeekTable
from ..models.kakebo_week_table import KakeboCostColors
from ..utils import get_data_row_from_kakebo_week, get_user_from_user_kakebo_composed

register = template.Library()


def render_sidebar_in_week_table(
    kakebo: KakeboWeek, row: int, color: str, total_row: int
) -> str:
    """Render sidebar in week table.

    Args:
        kakebo (KakeboWeek): KakeboWeek instance.
        row (int): Row number.
        color (str): Color string.
        total_row (int): Total row number.

    Returns:
        str: Render sidebar in week table.
    """
    html = """
        <td class="m-3" width="7.4%">
    """
    type_cost_index = int(KakeboCostColors.colors_costs.index(color))
    kakebo_week_table = KakeboWeekTable.objects.get(
        kakebo=kakebo, type_cost=type_cost_index
    )

    if row == total_row:
        text_desc, value = _("total"), kakebo_week_table.display_total_table
        html += f'<p class="mx-3 p-1 bg-{color} text-white">'
    else:
        data = kakebo_week_table.get_list_sort_cost(total_row)
        text_desc, value = (
            (data[row]["desc"], data[row]["value"])
            if data and row < len(data)
            else ("", "")
        )
        html += '<p class="p-3">'

    html += f"""
                {text_desc}
            </p>
        </td>
        <td class="p-3" width="5%">
            <p class="bb-dashed-{color} mb-2 text-end">
                € {value}
            </p>
        </td>
    """
    return html


@register.simple_tag
def white_space_table() -> str:
    """A simple body to render a white space.

    Returns:
        str: Return html to render a white space.
    """
    html = """
    <tbody>
        <tr>
            <td>
                <br>
            </td>
        </tr>
    </tbody>
    """
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_table_in_week(
    user_kakebo_composed: str,
    type_cost: str,
    rows: int = 7,
    disabled: bool = False,
) -> str:
    """Render table week.

    Args:
        user_kakebo_composed (str): Value composed of user_val, year, week in one word
            (e.g. 'username-year-week').
        type_cost (str): Cost typology from KakeboCostColors.
        rows (int, optional): Number of rows. Defaults to 7.
        disabled (bool, optional): If True, disable modal input. Defaults to False.

    Returns:
        str: Return the render table week.
    """
    cost_name, color = getattr(KakeboCostColors, type_cost)
    user, kakebo_month = get_user_from_user_kakebo_composed(
        user_kakebo_composed, week_composed=True
    )
    kakebo_week = KakeboWeek.objects.get(
        user=user, month=kakebo_month, week=int(user_kakebo_composed.split("-")[2]) - 1
    )

    html = "<tbody>"
    for row in range(rows):
        html += "<tr>"
        if row == 0:
            html += f"""
            <td class="align-top text-end p-3" rowspan="{rows}">
                <h5 class="text-{color}">
                    {cost_name}
                </h5>
            </td>
            """
        for clm in range(NUMBER_OF_DAYS_IN_WEEK):
            if row == 0:
                html += f'<td class="bt-8-{color} bx-{color} pt-3 px-15">'
            elif row == rows - 1:
                html += f'<td class="bb-{color} bx-{color} px-15">'
            else:
                html += f'<td class="bx-{color} px-15">'

            html += f"""
                <p class="w-100 mb-2 bb-dashed-{color} text-end">
            """

            data_row = get_data_row_from_kakebo_week(kakebo_week, cost_name, row, clm)
            html += (
                f"{data_row['desc'][:15]} => € {'%.2f' % data_row['value']}"
                if data_row is not None
                else "<br />"
            )

            tag_name_modal = f"tag_name_{color}_{clm}_{row}"
            if not disabled:
                html += f"""
                        <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#{tag_name_modal}">
                            <i class="bi bi-pencil-square"></i>
                        </button>
                    </p>
                """

            html += "</p></td>"

            if not disabled:
                html += f"""
                <div class="modal fade" id="{tag_name_modal}" tabindex="-1"
                    aria-labelledby="{tag_name_modal}_label" aria-hidden="true">
                    <div class="modal-dialog modal-lg modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="{tag_name_modal}_label">
                                    Descrizione e valore
                                </h5>
                                <button type="button" class="btn-close"
                                    data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                    
                                <div class="form-group row">
                                    <div class="col-sm-10">
                                        <label class="col-form-label">
                                            Descrizione:
                                        </label>
                                        <textarea class="form-control" id="id_{tag_name_modal}_desc" 
                                            name="{tag_name_modal}_desc" rows="4" cols="50"
                """

                html += 'placeholder="description">'
                html += data_row["desc"] if data_row is not None else ""
                html += "</textarea>"

                html += f"""
                                    </div>
                                    <div class="col-sm-2">
                                        <label class="col-form-label">
                                            Valore:
                                        </label>
                                        <input type="number" class="form-control" id="id_{tag_name_modal}_value"
                                            name="{tag_name_modal}_value" style="border: 1px solid grey"
                                            placeholder="0.00" min="0" step="0.01"
                """

                html += f"value={data_row['value']}>" if data_row is not None else ">"

                html += """
                                    </div>
                                </div>
    
                            </div>
                            <div class="modal-footer">
                                <button type="submit" class="btn btn-primary">
                                    Salva
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                """

        html += (
            render_sidebar_in_week_table(kakebo_week, row, color, rows - 1) + "</tr>"
        )
    html += "</tbody>"
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_table_total(list_total_costs: list[str]) -> str:
    """Render table total.

    Args:
        list_total_costs (list[str]): List with all total costs.

    Returns:
        str: Render table total.
    """
    html = """
    <tbody>
        <tr>
            <td class="align-top text-end p-3" rowspan="{row}">
                <h5 class="text-slategrey">
    """
    html += _("total")
    html += """
                </h5>
            </td>
    """
    for total_cost in list_total_costs:
        html += f"""
            <td class="b-slategrey px-15">
                <p class="bb-dashed-slategrey mb-0 text-end">
                    {total_cost} €
                </p>
            </td>
        """
    html += f"""
            <td class="px-15">
                <p class="bg-slategrey mb-0 px-1 text-white">
                    totale della settimana
                </p>
            </td>
            <td class="b-slategrey px-15">
                <p class="bb-dashed-slategrey mb-0 text-end">
                    {sum(list(map(float, list_total_costs)))} €
                </p>
            </td>
        </tr>
    </tbody>
    """
    return mark_safe(html)
