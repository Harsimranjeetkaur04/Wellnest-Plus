# dashboard/utils.py

from datetime import timedelta
from django.utils import timezone
from appointments.models import Appointment

def get_weekly_patient_stats(doctor):
    today = timezone.now().date()
    start_date = today - timedelta(days=6)

    labels = []
    data = []

    for i in range(7):
        day = start_date + timedelta(days=i)
        count = Appointment.objects.filter(doctor=doctor, date=day).count()
        labels.append(day.strftime("%a"))  # Mon, Tue, ...
        data.append(count)

    return labels, data
