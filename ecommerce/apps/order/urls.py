from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("add/", views.add, name="add"),
    path("", views.user_orders, name="user_orders"),
]
