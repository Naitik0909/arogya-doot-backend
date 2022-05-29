from django.contrib import admin
from django.urls import path, include

from .views import PatientListAPI, RegisterPatient, PatientDetailsAPI

urlpatterns = [
    path("register/", RegisterPatient.as_view(), name="register"),
    path("patient_details/<int:pk>/", PatientDetailsAPI.as_view()),
    path("patient_list/", PatientListAPI.as_view())

]