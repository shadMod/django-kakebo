from django import forms
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
