from django.db import models
from django.contrib.auth.models import User

from patient.models import Patient
from nurse.models import Nurse

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='Nurse/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return self.name

class Bed(models.Model):
    bed_type = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Observation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    observation = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name