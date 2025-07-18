from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from appointments.models import Appointment
from diagnosis.models import Diagnosis
from dashboard.utils import get_weekly_patient_stats
from accounts.models import Doctor

@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    today = timezone.now().date()

    # Filters
    query_date = request.GET.get("date")
    query_status = request.GET.get("status")
    query_patient = request.GET.get("patient")

    upcoming_appointments = Appointment.objects.filter(doctor=doctor)

    if query_date:
        upcoming_appointments = upcoming_appointments.filter(date=query_date)

    if query_status:
        upcoming_appointments = upcoming_appointments.filter(status=query_status)

    if query_patient:
        upcoming_appointments = upcoming_appointments.filter(
            Q(patient__first_name__icontains=query_patient) |
            Q(patient__last_name__icontains=query_patient)
        )

    # Stats
    appointments_today_count = upcoming_appointments.filter(date=today).count()
    patients_this_week = Appointment.objects.filter(
        doctor=doctor,
        date__range=(today - timedelta(days=7), today)
    ).values("patient").distinct().count()

    total_patients = Appointment.objects.filter(doctor=doctor).values("patient").distinct().count()

    weekly_visits_labels, weekly_visits_data = get_weekly_patient_stats(doctor)
    confirmed_count = upcoming_appointments.filter(status="CONFIRMED").count()
    pending_count = upcoming_appointments.filter(status="PENDING").count()

    recent_diagnoses = Diagnosis.objects.filter(doctor=doctor).order_by("-created_at")[:5]

    context = {
        "doctor": doctor,
        "upcoming_appointments": upcoming_appointments.order_by("date", "time"),
        "appointments_today_count": appointments_today_count,
        "patients_this_week": patients_this_week,
        "total_patients": total_patients,
        "weekly_visits_labels": weekly_visits_labels,
        "weekly_visits_data": weekly_visits_data,
        "confirmed_count": confirmed_count,
        "pending_count": pending_count,
        "recent_diagnoses": recent_diagnoses,
        "query_date": query_date or "",
        "query_status": query_status or "",
        "query_patient": query_patient or "",
    }

    return render(request, "dashboard/doctor_dashboard.html", context)



@login_required
def patient_dashboard(request):
    user = request.user

    # Safely check if user is a patient
    if hasattr(user, 'patient'):
        patient = user.patient

        appointments = Appointment.objects.filter(
            patient=patient,
            date__gte=timezone.now().date()  # all future appointments
        ).order_by('date', 'time')

        diagnoses = Diagnosis.objects.filter(patient=patient).order_by('-created_at')

        return render(request, 'dashboard/dashboard_patient.html', {
            'appointments': appointments,
            'diagnoses': diagnoses,
        })

    else:
        return redirect('doctor_dashboard')  # or a 403 page


