from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("register/", views.RegisterDoctor.as_view(), name="register_doctor"),
    path("doctor_info/<int:pk>/", views.DoctorDetail.as_view()),
    path("treatment/", views.DoctorTreatmentAPI.as_view()),
    path("observation/", views.DoctorObservation.as_view()),
    path("top_doctors/", views.TopDoctorsAPI.as_view())
]