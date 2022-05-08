from django.contrib import admin
from django.urls import path, include

from .views import RegisterDoctor

urlpatterns = [
    path("register/", RegisterDoctor.as_view(), name="register_doctor"),
]