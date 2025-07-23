from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

from appointments.models import Appointment
from diagnosis.models import Diagnosis
from accounts.models import Doctor


# ===========================
# Doctor Dashboard
# ===========================
@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('home')

    now = timezone.now()
    today = now.date()
    current_time = now.time()

    # Base queryset
    appointments_qs = Appointment.objects.filter(doctor=doctor).filter(
        Q(date__gt=today) |
        Q(date=today, time__gte=current_time)
    )

    # Filters
    query_date = request.GET.get("date")
    query_status = request.GET.get("status")
    query_patient = request.GET.get("patient")

    if query_date:
        appointments_qs = appointments_qs.filter(date=query_date)

    if query_status:
        appointments_qs = appointments_qs.filter(status=query_status)

    if query_patient:
        appointments_qs = appointments_qs.filter(
            Q(patient__first_name__icontains=query_patient) |
            Q(patient__last_name__icontains=query_patient)
        )

    # Stats
    appointments_today_count = appointments_qs.filter(date=today).count()

    patients_this_week = Appointment.objects.filter(
        doctor=doctor,
        date__range=(today - timedelta(days=7), today)
    ).values("patient").distinct().count()

    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values("patient").distinct().count()

    recent_diagnoses = Diagnosis.objects.filter(
        doctor=doctor
    ).order_by("-created_at")[:5]

    # Chart Data for Weekly Visits
    weekly_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_visits_labels = [day.strftime("%a") for day in weekly_dates]
    weekly_visits_data = [
        Appointment.objects.filter(doctor=doctor, date=day).count()
        for day in weekly_dates
    ]

    # Visited & Not Visited Appointments (static on dashboard)
    visited_qs = Appointment.objects.filter(
        doctor=doctor,
        status='CONFIRMED'
    ).filter(
        Q(date__lt=today) |
        Q(date=today, time__lt=current_time)
    ).order_by('-date', '-time')

    not_visited_qs = Appointment.objects.filter(
        doctor=doctor,
        status='CONFIRMED'
    ).filter(
        Q(date__gt=today) |
        Q(date=today, time__gte=current_time)
    ).order_by('date', 'time')

    visited_count = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).filter(
        Q(date__lt=today) |
        Q(date=today, time__lt=current_time)
    ).count()

    not_visited_count = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).filter(
        Q(date__gt=today) |
        Q(date=today, time__gte=current_time)
    ).count()

    context = {
        "doctor": doctor,
        "upcoming_appointments": appointments_qs.order_by("date", "time"),
        "appointments_today_count": appointments_today_count,
        "patients_this_week": patients_this_week,
        "total_patients": total_patients,
        "confirmed_count": appointments_qs.filter(status="CONFIRMED").count(),
        "pending_count": appointments_qs.filter(status="PENDING").count(),
        "recent_diagnoses": recent_diagnoses,
        "query_date": query_date or "",
        "query_status": query_status or "",
        "query_patient": query_patient or "",
        "weekly_visits_labels": weekly_visits_labels,
        "weekly_visits_data": weekly_visits_data,
        "visited_appointments": visited_qs,
        "not_visited_appointments": not_visited_qs,
        "visited_count" : visited_count,
        "not_visited_count": not_visited_count,
    }
    return render(request, "dashboard/doctor_dashboard.html", context)


# ===========================
# Patient Dashboard
# ===========================
@login_required
def patient_dashboard(request):
    user = request.user

    if not hasattr(user, 'is_patient') or not user.is_patient:
        messages.error(request, "Access denied. You are not registered as a patient.")
        return redirect('home')

    now = timezone.now()
    today = now.date()

    appointments = Appointment.objects.filter(
        patient=user,
        date__gte=today,
        status__in=["PENDING", "CONFIRMED"]
    ).order_by("date", "time")

    diagnoses = Diagnosis.objects.filter(
        patient=user
    ).order_by("-created_at")

    return render(request, 'dashboard/dashboard_patient.html', {
        'appointments': appointments,
        'diagnoses': diagnoses,
    })


# ===========================
# Visited Appointments (Separate Page)
# ===========================
@login_required
def visited_appointments_view(request):
    doctor = request.user.doctor
    now = timezone.now()

    visited = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).filter(
        Q(date__lt=now.date()) |
        Q(date=now.date(), time__lt=now.time())
    ).order_by("-date", "-time")

    not_visited = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).exclude(id__in=visited.values_list("id", flat=True)).order_by("date", "time")

    context = {
        "visited_appointments": visited,
        "not_visited_appointments": not_visited,
    }
    return render(request, "appointments/visited_appointment.html", context)
