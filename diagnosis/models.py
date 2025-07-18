from django.db import models
from accounts.models import CustomUser, Doctor
from appointments.models import Appointment  # if appointment model exists

class Diagnosis(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='diagnoses')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    symptoms = models.TextField(blank=True, null=True)  # Optional if no AI used
    prediction = models.CharField(max_length=100, blank=True, null=True)  # Optional (AI use case)
    diagnosed_disease = models.CharField(max_length=100)  # ✅ Doctor will always fill this
    notes = models.TextField(blank=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.diagnosed_disease} - {self.patient.get_full_name()}"
