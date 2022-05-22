from django.db import models
from django.contrib.auth.models import User

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
    age = models.IntegerField(max_length=4, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    working_days = models.CharField(max_length=20, null=True, blank=True)
  
    specialization = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    profile_pic = models.ImageField(upload_to='Doctor/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Treatment(models.Model):

    TREATMENT_CHOICES = (
        ("Temperature", "Temperature"),
        # ("Temperature", "Temperature"),
        # ("Temperature", "Temperature"),
        # ("Temperature", "Temperature"),
        
    )

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment_type = models.CharField(max_length=50, null=True, blank=True, choices=TREATMENT_CHOICES)
    treatment_value = models.CharField(max_length=100, null=True, blank=True)
    detail = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    
