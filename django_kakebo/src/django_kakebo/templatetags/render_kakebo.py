from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def white_space_table():
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
def render_table(color: str, row: int = 7, name: str = None):
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
        for cell in range(7):
            if i == 0:
                html += f'<td class="bt-8-{color} bx-{color} px-15">'
            elif i == 6:
                html += f'<td class="bb-{color} bx-{color} px-15">'
            else:
                html += f'<td class="bx-{color} px-15">'
            html += f"""
                <p class="bb-dashed-{color} mb-2">
                    <input>
                </p>
            </td>
            """
        html += "</tr>"
    html += "</tbody>"
    return mark_safe(html)


@register.filter(is_safe=True)
@register.simple_tag
def render_table_total(row: int = 7):
    html = """
    <tbody>
        <tr>
            <td class="align-top text-end p-3" rowspan="{row}">
                <h5 class="text-slategrey">
                    totale
                </h5>
            </td>
    """
    for i in range(row):
        html += """
            <td class="b-slategrey px-15">
                <p class="bb-dashed-slategrey mb-0">
                    <input>
                </p>
            </td>
        """
    html += """
        </tr>
    </tbody>
    """
    return mark_safe(html)
