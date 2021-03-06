from multiprocessing.dummy import Array
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from patient.models import Patient
from nurse.models import Nurse

class Doctor(models.Model):

    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),

    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    aadhaar = models.CharField(max_length=15, null=True, blank=True)
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=5, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    working_days = ArrayField(models.IntegerField(blank=True),size=8, null=True, blank=True)
  
    specialization = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    profile_pic = models.ImageField(upload_to='Doctor/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Treatment(models.Model):

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.CharField(max_length=20, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    treatment_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    status = models.BooleanField(default=False)
    
class Observation(models.Model):

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    temperature = models.CharField(max_length=20, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    oxygen_level = models.CharField(max_length=20, null=True, blank=True)
    heart_rate = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)