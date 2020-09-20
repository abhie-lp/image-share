from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),
    path("password-reset/", auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path("password-change/", auth_views.PasswordChangeView.as_view(),
         name="password_change"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
    path("", views.dashboard, name="dashboard"),
]
