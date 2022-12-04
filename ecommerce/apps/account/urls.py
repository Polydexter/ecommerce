from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm

app_name = "account"

urlpatterns = [
    path("register/", views.account_register, name="register"),
    path(
        "activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html", form_class=UserLoginForm
        ),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="../login/"), name="logout"
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="account/password/reset_status.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password_reset_confirm.html",
            success_url="/account/password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(template_name="account/password/reset_status.html"),
        name="password_resset_complete",
    ),
    # User dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),
        name="delete_confirm",
    ),
    path("addresses/", views.address_list, name="addresses"),
    path("address_add/", views.address_add, name="address_add"),
    path("addresses/edit/<slug:id>/", views.address_edit, name="address_edit"),
    path("addresses/delete/<slug:id>/", views.address_delete, name="address_delete"),
    path(
        "addresses/set_default/<slug:id>/",
        views.address_set_default,
        name="address_set_default",
    ),
    # Wishlist
    path("wishlist", views.wishlist, name="wishlist"),
    path(
        "add_to_wishlist/<int:id>/",
        views.wishlist_product_toggle,
        name="wishlist_product_toggle",
    ),
]
