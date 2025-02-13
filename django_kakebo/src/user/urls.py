from django.contrib.auth import views as auth_view
from django.urls import path, include

from user.views import (
    RegisterFormView,
    AccountLoginView,
    AccountPasswordResetView,
    AccountPasswordResetDoneView,
    AccountPasswordResetConfirmView,
    AccountPasswordResetCompleteView,
)

urlpatterns = [
    path("accounts/sign-up/", RegisterFormView.as_view(), name="sign_up"),
    # path(
    #     "accounts/active/<uidb64:uidb64>/<str:token>",
    #     active_user_mail_token,
    #     name="active-user-mail-token",
    # ),
    path("accounts/login/", AccountLoginView.as_view(), name="login"),
    path(
        "accounts/logout/",
        auth_view.LogoutView.as_view(
            template_name="user/sign-out.html",
        ),
        name="logout",
    ),
    path(
        "accounts/password/change/",
        auth_view.PasswordChangeView.as_view(
            template_name="user/password-change.html",
        ),
        name="password_change",
    ),
    path(
        "accounts/password/change/conferma",
        auth_view.PasswordChangeDoneView.as_view(
            template_name="user/password-change-done.html",
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password/reset/",
        AccountPasswordResetView.as_view(),
        name="password_change_done",
    ),
    path(
        "accounts/password/reset/thanks/",
        AccountPasswordResetDoneView.as_view(),
        name="reset_password",
    ),
    path(
        "accounts/password/reset/confirm/<uidb64>/<token>/",
        AccountPasswordResetConfirmView.as_view(),
        name="reset_password_done",
    ),
    path(
        "accounts/password/reset/complete/",
        AccountPasswordResetCompleteView.as_view(),
        name="reset_password_confirm",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
