from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(),
    )
    condition_check = forms.BooleanField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": self.fields[field].label,
                }
            )

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password2 = data.get("password2")
        if password2 != password:
            raise forms.ValidationError(_("Passwords aren't the same"))

        condition_check = data.get("condition_check")
        if condition_check is False:
            raise forms.ValidationError(_("You must accept the conditions of sale"))
        return data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(_("Email already in use"))
        return email


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": str(field).capitalize(),
                }
            )
