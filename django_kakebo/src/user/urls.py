from django.urls import path, include
from django.contrib.auth import views as auth_view

from .views import (
    RegisterPageFormView,
    # active_user_mail,
    AccountLoginView,
    AccountPasswordResetView,
    AccountPasswordResetDoneView,
    AccountPasswordResetConfirmView,
    AccountPasswordResetCompleteView,
)

urlpatterns = []

urlpatterns += [
    path(
        "sign_up/",
        RegisterPageFormView.as_view(),
        name="sign_up",
    ),
    # path(
    #     "active/<str:uidb64>/<str:token>",
    #     active_user_mail,
    #     name="active-user-mail",
    # ),
    path(
        "login/",
        AccountLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_view.LogoutView.as_view(
            template_name="user/sign-out.html",
        ),
        name="logout",
    ),
    path(
        "password/change/",
        auth_view.PasswordChangeView.as_view(
            template_name="user/password-change.html",
        ),
        name="password_change",
    ),
    path(
        "password/change/conferma",
        auth_view.PasswordChangeDoneView.as_view(
            template_name="user/password-change-done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password/reset/",
        AccountPasswordResetView.as_view(),
        name="password_change_done",
    ),
    path(
        "password/reset/thanks/",
        AccountPasswordResetDoneView.as_view(),
        name="reset_password",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        AccountPasswordResetConfirmView.as_view(),
        name="reset_password_done",
    ),
    path(
        "password/reset/complete/",
        AccountPasswordResetCompleteView.as_view(),
        name="reset_password_confirm",
    ),
]

urlpatterns += [
    path("", include("django.contrib.auth.urls")),
]
