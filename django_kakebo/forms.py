from itertools import product

from django import forms
from django.forms import formset_factory

from .constants import (
    NUMBER_OF_DAYS_IN_WEEK,
    ROW_TABLE_NUMBER,
    NUMBER_OF_ANSWER,
    CashFlowType,
)
from .models.kakebo_week_table import KakeboCostColors


class KakeboWeekForm(forms.Form):
    """Kakebo week form."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize form and add color fields with related tags (tag_name, description and value)."""
        super(KakeboWeekForm, self).__init__(*args, **kwargs)
        tag_fields = [
            f"tag_name_{color}_{day}_{table_row}"
            for color, table_row, day in product(
                KakeboCostColors.colors_costs,
                range(ROW_TABLE_NUMBER),
                range(NUMBER_OF_DAYS_IN_WEEK),
            )
        ]
        for tag_name in tag_fields:
            self.fields[f"{tag_name}_desc"] = forms.CharField(
                max_length=200, required=False
            )
            self.fields[f"{tag_name}_value"] = forms.FloatField(required=False)


class SelectYearWeekForm(forms.Form):
    """Select year week form."""

    spare_cost = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}), required=False
    )
    target_reach = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}), required=False
    )
    spare = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize form and add 'income' and 'outflow' fields."""
        super(SelectYearWeekForm, self).__init__(*args, **kwargs)
        for field in CashFlowType:
            self.fields[f"date_{field.value}"] = forms.DateField(required=False)
            self.fields[f"descr_{field.value}"] = forms.CharField(
                max_length=200, required=False
            )
            self.fields[f"value_{field.value}"] = forms.FloatField(required=False)


SelectYearWeekFormSet = formset_factory(SelectYearWeekForm, extra=2)


class EndOfMonthBalanceSheetForm(forms.Form):
    """End of month balance sheet form."""

    electricity = forms.FloatField(required=False)
    gas = forms.FloatField(required=False)
    tel_internet = forms.FloatField(required=False)
    water = forms.FloatField(required=False)
    waste = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize form and add 'cost' fields."""
        conclusion = kwargs["initial"]["conclusion"]
        super(EndOfMonthBalanceSheetForm, self).__init__(*args, **kwargs)

        for answer_number in range(NUMBER_OF_ANSWER):
            # TODO: answer_number with +1 or less?
            self.fields[f"answer_{answer_number}"] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": "5"}), required=False
            )

        for index_cost in range(2):
            self.fields[f"cost_{index_cost}_name"] = forms.CharField(
                max_length=200, required=False
            )
            for cost_row in range(1, 6):
                self.fields[f"cost_{index_cost}_{cost_row}"] = forms.FloatField(
                    required=False
                )

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            if conclusion and field != "answer_3":
                self.fields[field].widget.attrs["disabled"] = "disabled"
