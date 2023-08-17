import requests

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

from .forms import RegisterForm, AuthForm


class RegisterPageFormView(FormView):
    form_class = RegisterForm
    template_name = "user/sign-up.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.get_success_url()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        request = self.request
        cd = form.cleaned_data

        username = cd["username"]
        email = cd["email"]
        password = cd["password"]

        if getattr(settings, 'GOOGLE_RECAPTCHA_SECRET_KEY', None) is not None:
            """ Start reCAPTCHA validation """
            res = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": res,
            }
            response = requests.post(url=url, data=values)
            result = response.json()
            """ End reCAPTCHA validation """

            if not result.get("success"):
                form.add_error(field=None, error="Verifica Captcha fallita")
                return self.form_invalid(form)

        User.objects.create_user(
            username, email, password
        )
        messages.success(request, "Utente creato con successo, controlla la mail per confermarla")
        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(reverse_lazy("login"))


def active_user_mail():
    pass


class AccountLoginView(LoginView):
    """
    Display the custom login form and handle the login action.
    """

    form_class = AuthForm
    template_name = "user/sign-in.html"
    success_url = reverse_lazy("index")


class AccountPasswordResetView(PasswordResetView):
    pass


class AccountPasswordResetDoneView(PasswordResetDoneView):
    pass


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    pass


class AccountPasswordResetCompleteView(PasswordResetDoneView):
    pass
