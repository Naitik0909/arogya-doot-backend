from django.contrib import admin
from django.urls import path

from .views import RegisterNurse

urlpatterns = [
    path("register/", RegisterNurse.as_view(), name="register_nurse"),
]