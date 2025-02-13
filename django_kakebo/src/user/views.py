from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from user.forms import RegisterForm, AuthForm
from user.utils import validate_recaptcha


class RegisterFormView(FormView):
    """Register form view."""

    form_class = RegisterForm
    template_name = "user/sign-up.html"

    def dispatch(self, *args, **kwargs) -> HttpResponse:
        """Dispatch method to register form.

        Returns:
            HttpResponse: HTTP response.
        """
        if self.request.user.is_authenticated:
            return self.get_success_url()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form: RegisterForm) -> HttpResponseRedirect:
        """Validate form, check recaptcha if active and create a new User if not exists.

        Args:
            form (RegisterForm): Register form.

        Returns:
            HttpResponseRedirect: HTTP response redirect.
        """
        cd = form.cleaned_data
        username = cd["username"]
        email = cd["email"]
        password = cd["password"]

        if getattr(settings, "GOOGLE_RECAPTCHA_SECRET_KEY", None) is not None:
            result = validate_recaptcha(self.request.POST.get("g-recaptcha-response"))
            if not result.get("success"):
                form.add_error(field=None, error=_("Captcha verification failed."))
                return self.form_invalid(form)

        User.objects.create_user(username, email, password)
        messages.success(
            self.request,
            _("User created successfully, check email to confirm."),
        )
        return self.get_success_url()

    def get_success_url(self) -> HttpResponseRedirect:
        """Get login url.

        Returns:
            HttpResponseRedirect: HTTP response redirect.
        """
        return HttpResponseRedirect(reverse_lazy("login"))


class AccountLoginView(LoginView):
    """Display the custom login form and handle the login action."""

    form_class = AuthForm
    template_name = "user/sign-in.html"
    success_url = reverse_lazy("index")


class AccountPasswordResetView(PasswordResetView):
    """Account password reset view."""


class AccountPasswordResetDoneView(PasswordResetDoneView):
    """Account password reset done view."""


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    """Account password reset confirm view."""


class AccountPasswordResetCompleteView(PasswordResetDoneView):
    """Account password reset complete view."""
