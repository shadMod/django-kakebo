from django import template
from django.utils.safestring import mark_safe
from django_kakebo.constants import colors as list_colors
from django.contrib.auth.models import User
from django_kakebo.models import KakeboWeek, KakeboWeekTable

register = template.Library()


def get_data_byobj(kakebo: dict, color: str, row: int, column: int):
    key_color = int(list_colors.index(color))
    kakebo = KakeboWeekTable.objects.get(
        kakebo=kakebo, type_cost=key_color
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
def render_table(color: str = None, row: int = 7, name: str = None, kakebo: str = None):
    """
    Render table with a determinate color and row
    """
    if color is None:
        color = "orange"

    # get kakebo table week from db
    username, year, week = kakebo.split('-')
    user = User.objects.get(username=username)
    obj = KakeboWeek.objects.get(
        user=user, year=year, week=week,
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
                html += f'<td class="bt-8-{color} bx-{color} px-15">'
            elif i == row - 1:
                html += f'<td class="bb-{color} bx-{color} px-15">'
            else:
                html += f'<td class="bx-{color} px-15">'

            data_ = get_data_byobj(obj, color, i, clm)

            tag_name_modal = f"tag_name_{color}_{clm}_{i}"
            html += f"""
                <p class="bb-dashed-{color} mb-2 text-end">
                    <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#{tag_name_modal}">
            """
            if data_ is not None:
                html += f"""
                    {data_['desc'][:15]} => € {'%.2f' % data_['value']}
                """
            html += f"""
                        <i class="bi bi-pencil-square"></i>
                    </button>
                </p>
            </td>
            
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
        html += "</tr>"
    html += "</tbody>"
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_table_total(totals: list):
    html = """
    <tbody>
        <tr>
            <td class="align-top text-end p-3" rowspan="{row}">
                <h5 class="text-slategrey">
                    totale
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
    html += """
        </tr>
    </tbody>
    """
    return mark_safe(html)
