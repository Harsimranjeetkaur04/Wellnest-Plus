from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SymptomRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    predicted_condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_condition} ({self.created_at.date()})"

