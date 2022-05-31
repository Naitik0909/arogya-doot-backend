from django.db import models
from django.contrib.auth.models import User

from patient.models import Patient
# from nurse.models import Nurse

class Nurse(models.Model):

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
    patients = models.ManyToManyField("patient.Patient", blank=True)

    profile_pic = models.ImageField(upload_to='Nurse/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_day_shift = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name

class Bed(models.Model):

    BED_TYPE_CHOICES = (
        ("General", "General"),
        ("Private", "Private"),
        ("Deluxe", "Deluxe"),


    )

    bed_type = models.CharField(choices=BED_TYPE_CHOICES, max_length=100, null=True, blank=True)
    number = models.CharField(max_length=100, null=True, blank=True)
    room_no = models.CharField(max_length=20, null=True, blank=True)
    floor_no = models.CharField(max_length=20, null=True, blank=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.number