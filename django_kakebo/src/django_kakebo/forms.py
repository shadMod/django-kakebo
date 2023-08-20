from django import forms
from django.forms import formset_factory, inlineformset_factory

from .constants import colors


class KakeboWeekForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(KakeboWeekForm, self).__init__(*args, **kwargs)

        for color in colors:
            for row in range(9):  # casual max value (number)
                for clm in range(7):  # 7 days in one week
                    tag_name = f"tag_name_{color}_{clm}_{row}"
                    self.fields[f"{tag_name}_desc"] = forms.CharField(
                        max_length=200, required=False
                    )
                    self.fields[f"{tag_name}_value"] = forms.FloatField(
                        required=False
                    )


class SelectYearWeekForm(forms.Form):
    spare_cost = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}), required=False)
    target_reach = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}), required=False)
    spare = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs):
        super(SelectYearWeekForm, self).__init__(*args, **kwargs)

        field_types = ["income", "outflow"]
        for field in field_types:
            self.fields[f"date_{field}"] = forms.DateField(
                required=False
            )
            self.fields[f"descr_{field}"] = forms.CharField(
                max_length=200, required=False
            )
            self.fields[f"value_{field}"] = forms.FloatField(
                required=False
            )


SelectYearWeekFormSet = formset_factory(SelectYearWeekForm, extra=2)
