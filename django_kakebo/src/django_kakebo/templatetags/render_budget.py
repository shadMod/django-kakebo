from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ..models import KakeboMonth

register = template.Library()


@register.filter(is_safe=True)
@register.simple_tag
def render_month_budget(kakebo: str, section: str, nr_row: int = 4, disabled: bool = False):
    username, month, year = kakebo.split('-')
    user = User.objects.get(username=username)
    obj = KakeboMonth.objects.get(
        user=user, month=month, year=year
    )
    budget = obj.budget
    disabled = "disabled" if disabled else ""

    html = ""
    for i in range(nr_row):
        value = budget.get(f"_{section}_{i}")
        val_date, val_descr, val_value = "", "", ""
        if value:
            val_date = value.get(f"date_{section}")
            val_descr = value.get(f"descr_{section}")
            val_value = "%.2f" % value.get(f"value_{section}")

        html += f"""
        <tr>
            <td></td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{i}-date_{section}" id="id_form-{i}-date_{section}"
                        type="date" value="{val_date}" {disabled}>
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{i}-descr_{section}" id="id_form-{i}-descr_{section}"
                    value="{val_descr}" {disabled}>
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{i}-value_{section}" id="id_form-{i}-value_{section}"
                    value="{val_value}" {disabled}>
                </p>
            </td>
        </tr>
        """

    total_ = [
        (_("total income"), "cyan", obj.display_totals_budget[0]),
        (_("total steady outflow"), "blue", obj.display_totals_budget[1])
    ]
    total_ = total_[0] if section == 'income' else total_[1]
    html += f"""
        <tr>
            <td></td>
            <td colspan="2" class="bs-10-white">
                <p class="w-100 pt-3 ps-3 bg-{total_[1]}-basic text-white">
                    {total_[0]}
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    € {total_[2]}
                </p>
            </td>
        </tr>
    """
    return mark_safe(html)
