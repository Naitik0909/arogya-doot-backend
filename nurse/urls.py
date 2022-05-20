from unicodedata import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterNurse.as_view(), name="register_nurse"),
    path("dashboard/", views.NurseDashboard.as_view(), name="dashboard"),
    path("treatments/", views.NurseTreatmentAPI.as_view())
]