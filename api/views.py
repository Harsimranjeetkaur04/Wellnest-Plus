from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from accounts.models import CustomUser
from appointments.models import Appointment
from diagnosis.models import Diagnosis

# ✅ Patient preview for hover/click preview
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
            'status': 'Confirmed' if a.status == 'CONFIRMED' else 'Pending'
        } for a in appointments]

        last_diagnosis = Diagnosis.objects.filter(patient=user).order_by('-created_at').first()

        data = {
            'name': patient_name,
            'age': getattr(user, 'age', 'N/A'),
            'gender': getattr(user, 'gender', 'N/A'),
            'appointments': appointment_data,
            'last_diagnosis': last_diagnosis.diagnosed_disease if last_diagnosis else None
        }
        return JsonResponse(data)

    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)

# ✅ Appointment details for diagnosis preview
@login_required
def appointment_detail_api(request, appointment_id):
    try:
        app = Appointment.objects.get(id=appointment_id)
        diag = Diagnosis.objects.filter(appointment=app).last()

        return JsonResponse({
            "name": app.patient.get_full_name(),
            "date": app.date.strftime("%Y-%m-%d"),
            "time": app.time.strftime("%H:%M"),
            "issue": diag.diagnosed_disease if diag else None
        })

    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
