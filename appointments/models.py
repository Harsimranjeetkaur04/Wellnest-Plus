from django.db import models
from accounts.models import CustomUser, Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='PENDING')

    # ✅ Uncomment these if you actually want them:
    is_confirmed = models.BooleanField(default=False)
    symptoms = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} on {self.date}"
