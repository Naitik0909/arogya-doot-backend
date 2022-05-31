from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path("register/", RegisterPatient.as_view(), name="register"),
    path("patient_details/<int:pk>/", PatientDetailsAPI.as_view()),
    path("patient_list/", PatientListAPI.as_view()),
    path("current_patient_details/", CurrentPatientDetails.as_view()),
    path("observations/", PatientObservationsAPI.as_view()),
    path("treatments/", PatientTreatmentsAPI.as_view()),
    path("landing_stats/",LandingPageAPI.as_view()),
    path("landing_page_pie/", LandingPagePieAPI.as_view()),
    path("landing_page_graph/", LandingPageGraphAPI.as_view()),

]