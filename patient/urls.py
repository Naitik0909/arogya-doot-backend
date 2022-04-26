from django.contrib import admin
from django.urls import path, include

from .views import RegisterPatient

urlpatterns = [
    path("register/", RegisterPatient.as_view(), name="register"),
]