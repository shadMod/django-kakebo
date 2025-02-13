from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.Form):
    """Form for registering a new user."""

    username = forms.CharField(label=_("Username"), widget=forms.TextInput())
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput()
    )
    condition_check = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initialization form and put in all fields class 'form-control' and placeholder from related label."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": self.fields[field].label,
                }
            )

    def clean(self) -> dict[str, Any]:
        """Cleaning logic for registering a new user.

        Raises:
            ValidationError: If condition check is False or 'condition_check' key not exists.

        Returns:
            dict[str, Any]: form data for registering a new user.
        """
        data = self.cleaned_data
        password = data.get("password")
        password2 = data.get("password2")
        if password2 != password:
            raise forms.ValidationError(_("Passwords aren't the same"))
        if data.get("condition_check", False) is False:
            raise forms.ValidationError(_("You must accept the conditions of sale"))
        return data

    def clean_email(self) -> str:
        """Validate email from cleaned data.

        Raises:
            ValidationError: If yet a user with this email.

        Returns:
            str: Return if 'email' field is valid.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already in use"))
        return email


class AuthForm(AuthenticationForm):
    """Authentication form for authorizing user."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialization form for authorizing user."""
        super(AuthForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": str(field).capitalize(),
                }
            )
