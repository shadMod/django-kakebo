from enum import Enum

from django.utils.translation import gettext_lazy as _


class CashFlowType(Enum):
    income = "income"
    outflow = "outflow"


NUMBER_OF_DAYS_IN_WEEK = 7
NUMBER_OF_ANSWER = 3

NAMES_OF_THE_DAYS = [
    _("Monday"),
    _("Tuesday"),
    _("Wednesday"),
    _("Thursday"),
    _("Friday"),
    _("Saturday"),
    _("Sunday"),
]

DEFAULT_LIST_UTILITIES = ["electricity", "gas", "tel_internet", "water", "waste"]

ANSWER_SMILE_LIST = {
    "yes": "sunglasses",
    "almost": "expressionless",
    "no": "frown",
}

TOTAL_KAKEBO_MONTH_BUDGET = {
    CashFlowType.income.value: {
        "description": _("total income"),
        "color": "cyan",
        "display_property": "display_total_income_budget",
    },
    CashFlowType.outflow.value: {
        "description": _("total steady outflow"),
        "color": "blue",
        "display_property": "display_total_outflow_budget",
    },
}

# TODO: add management in back-office view
ROW_TABLE_NUMBER = 9
DEFAULT_ROWS_WEEK_FORM = [10, 7, 7, 7]
NUMBER_OF_COSTS_IN_REPORT = 2
