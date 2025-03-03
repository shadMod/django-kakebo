from django import template
from django.utils.safestring import mark_safe

from ..constants import CashFlowType, TOTAL_KAKEBO_MONTH_BUDGET
from ..utils import get_user_from_user_kakebo_composed

register = template.Library()


@register.filter(is_safe=True)
@register.simple_tag
def render_month_budget(
    user_kakebo_composed: str, section: str, rows: int = 4, disabled: bool = False
) -> str:
    """Render kakebo month budget.

    Args:
        user_kakebo_composed (str): Value composed of user_val, month, year in one word
            (e.g. 'username-month-year').
        section (str): Section name.
        rows (int, optional): Number of rows. Defaults to 5.
        disabled (bool, optional): If True, disable input cost. Defaults to False.

    Returns:
        str: Return the render kakebo month budget.
    """
    if section not in CashFlowType:
        raise ValueError("Invalid section.")

    user, kakebo_month = get_user_from_user_kakebo_composed(user_kakebo_composed)
    budget = kakebo_month.budget
    disabled = "disabled" if disabled else ""

    html = ""
    for row in range(rows):
        value = budget.get(f"_{section}_{row}", {})
        val_date = value.get(f"date_{section}", "")
        val_descr = value.get(f"descr_{section}", "")
        val_value = (
            "%.2f" % value[f"value_{section}"] if value.get(f"value_{section}") else 0
        )

        html += f"""
        <tr>
            <td></td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{row}-date_{section}" id="id_form-{row}-date_{section}"
                        type="date" value="{val_date}" {disabled}>
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{row}-descr_{section}" id="id_form-{row}-descr_{section}"
                    value="{val_descr}" {disabled}>
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    <input name="form-{row}-value_{section}" id="id_form-{row}-value_{section}"
                    value="{val_value}" {disabled}>
                </p>
            </td>
        </tr>
        """

    total_kakebo_month_dict = TOTAL_KAKEBO_MONTH_BUDGET[CashFlowType[section].value]
    html += f"""
        <tr>
            <td></td>
            <td colspan="2" class="bs-10-white">
                <p class="w-100 pt-3 ps-3 bg-{total_kakebo_month_dict["color"]}-basic text-white">
                    {total_kakebo_month_dict["description"]}
                </p>
            </td>
            <td class="bs-10-white">
                <p class="bb-dashed-slategrey w-100 pt-3">
                    € {getattr(kakebo_month, total_kakebo_month_dict["display_property"], 0)}
                </p>
            </td>
        </tr>
    """
    return mark_safe(html)
