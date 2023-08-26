from datetime import datetime

from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from ..constants import colors as list_colors
from ..models import KakeboMonth, KakeboWeek, KakeboWeekTable

register = template.Library()


def get_data_byobj(kakebo: dict, color: str, row: int, column: int):
    type_cost = int(list_colors.index(color))
    kakebo = KakeboWeekTable.objects.get(
        kakebo=kakebo, type_cost=type_cost
    ).data_row

    if not any(
            kakebo
            and kakebo.get(f"{column}", "")
            and kakebo.get(f"{column}", "").get(f"{row}", "")
    ):
        return None

    return kakebo[f"{column}"][f"{row}"]


@register.simple_tag
def white_space_table():
    # a simple body to render a white space
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
def render_table(color: str = None, row: int = 7, name: str = None, kakebo: str = None, disabled: bool = False):
    """
    Render table with a determinate color and row
    """
    if color is None:
        color = "orange"

    # get kakebo table week from db
    username, year, week = kakebo.split('-')
    # get user
    user = User.objects.get(username=username)
    date_w = f"{year}-{week}-1"
    # get KakeboMonth()
    month = KakeboMonth.objects.get(
        user=user,
        month=datetime.strptime(date_w, "%Y-%W-%w").month,
        year=year,
    )
    obj = KakeboWeek.objects.get(
        user=user, month=month, week=week,
    )

    html = "<tbody>"
    for i in range(row):
        html += "<tr>"
        if i == 0:
            html += f"""
            <td class="align-top text-end p-3" rowspan="{row}">
                <h5 class="text-{color}">
                    {name}
                </h5>
            </td>
            """
        for clm in range(7):  # 7 days in one week
            if i == 0:
                html += f'<td class="bt-8-{color} bx-{color} pt-3 px-15">'
            elif i == row - 1:
                html += f'<td class="bb-{color} bx-{color} px-15">'
            else:
                html += f'<td class="bx-{color} px-15">'

            data_ = get_data_byobj(obj, color, i, clm)

            tag_name_modal = f"tag_name_{color}_{clm}_{i}"
            html += f"""
                <p class="w-100 mb-2 bb-dashed-{color} text-end">
            """

            if data_ is not None:
                html += f"{data_['desc'][:15]} => € {'%.2f' % data_['value']}"
            else:
                html += "<br />"

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
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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
                html += data_["desc"] if data_ is not None else ""
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

                html += f"value={data_['value']}>" if data_ is not None else ">"

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
        # sidebar
        html += render_sidebar(obj, i, color, row - 1)
        # close row
        html += "</tr>"
    html += "</tbody>"
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_table_total(totals: list, total_week: int):
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
    for value in totals:
        html += f"""
            <td class="b-slategrey px-15">
                <p class="bb-dashed-slategrey mb-0 text-end">
                    {value} €
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
                {total_week} €
            </p>
        </td>
    """
    html += """
        </tr>
    </tbody>
    """
    return mark_safe(html)


def render_sidebar(kakebo, row: int, color: str, total_row: int):
    # init cell html
    html = f"""
        <td class="m-3" width="7.4%">
    """

    type_cost = int(list_colors.index(color))
    obj = KakeboWeekTable.objects.get(
        kakebo=kakebo, type_cost=type_cost
    )

    # init and set value
    if row == total_row:
        val = (_("total"), obj.display_total_table)
        html += f'<p class="mx-3 p-1 bg-{color} text-white">'
    else:
        data = obj.get_list_sort_cost(total_row)
        if data and row < len(data):
            data = data[row]
            val = (data['desc'], data['value'])
        else:
            val = ("", "")
        html += '<p class="p-3">'

    html += f"""
            {val[0]}
            </p>
        </td>
        <td class="p-3" width="5%">
            <p class="bb-dashed-{color} mb-2 text-end">
             € {val[1]}
            </p>
        </td>
    """
    return html
