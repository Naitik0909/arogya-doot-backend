from unicodedata import name
from django.contrib import admin
from django.urls import path

from .views import RegisterNurse, NurseDashboard

urlpatterns = [
    path("register/", RegisterNurse.as_view(), name="register_nurse"),
    path("dashboard/", NurseDashboard.as_view(), name="dashboard"),
    # path("observations/")
]