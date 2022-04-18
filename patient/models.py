from django.db import models
from django.contrib.auth.models import User

from doctor.models import Doctor

class Patient(models.Model):

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    profile_pic = models.ImageField(upload_to='Patient/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=100, null=True, blank=True)

    consulting_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name