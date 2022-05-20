from django.db import models
from django.contrib.auth.models import User

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

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),

    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age = models.CharField(max_length=4, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=100, null=True, blank=True)
    aadhaar = models.CharField(max_length=100, null=True, blank=True)

    profile_pic = models.ImageField(upload_to='Patient/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    consulting_doctor = models.ForeignKey("doctor.Doctor", on_delete=models.SET_NULL, null=True, blank=True)
    allocated_bed = models.OneToOneField("nurse.Bed", on_delete=models.SET_NULL, null=True, blank=True)

    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=100, null=True, blank=True)

    is_treated = models.BooleanField(default=False)

    

    def __str__(self):
        return self.user.first_name

class TreatmentHistory(models.Model):
    
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    nurse = models.ForeignKey('nurse.Nurse', on_delete=models.CASCADE)