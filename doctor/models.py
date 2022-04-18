from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='Doctor/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Treatment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
