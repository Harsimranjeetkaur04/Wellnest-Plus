# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    # 🆕 Additional Medical Info
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    known_allergies = models.TextField(blank=True)
    existing_conditions = models.TextField(blank=True)


    # Optional profile photo
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default="General")  # ✅ Added
    degree = models.CharField(max_length=100, default="Not specified")
    available_days = models.CharField(max_length=100, default="Mon-Fri")
    availability_time = models.CharField(max_length=100, default="9am-5pm")
    standard_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    special_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    contact = models.CharField(max_length=100, default="Not specified")
    profile_photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)  # 👈 new field

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.user.get_full_name() or self.user.username
