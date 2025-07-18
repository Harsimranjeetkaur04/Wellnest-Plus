from django.http import JsonResponse
from accounts.models import CustomUser
from appointments.models import Appointment
from diagnosis.models import Diagnosis
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

@login_required
@require_GET
def patient_preview_api(request, patient_id):
    try:
        user = CustomUser.objects.get(id=patient_id)
        patient_name = f"{user.first_name} {user.last_name}".strip() or user.username

        appointments = Appointment.objects.filter(patient=user).order_by('-date')[:3]
        appointment_data = [{
            'date': str(a.date),
            'time': str(a.time),
            'status': 'Confirmed' if a.is_confirmed else 'Pending'
        } for a in appointments]

        last_diagnosis = Diagnosis.objects.filter(patient=user).order_by('-date').first()

        data = {
            'name': patient_name,
            'age': user.age if hasattr(user, 'age') else 'N/A',
            'gender': user.gender if hasattr(user, 'gender') else 'N/A',
            'appointments': appointment_data,
            'last_diagnosis': last_diagnosis.disease if last_diagnosis else None
        }
        return JsonResponse(data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
