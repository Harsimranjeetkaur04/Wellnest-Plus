from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from appointments.models import Appointment
from diagnosis.models import Diagnosis
from accounts.models import Doctor
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

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

    appointments_qs = Appointment.objects.filter(doctor=doctor).filter(
        Q(date__gt=today) | Q(date=today, time__gte=current_time)
    )

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

    appointments_today_count = appointments_qs.filter(date=today).count()
    patients_this_week = Appointment.objects.filter(
        doctor=doctor,
        date__range=(today - timedelta(days=7), today)
    ).values("patient").distinct().count()
    total_patients = Appointment.objects.filter(doctor=doctor).values("patient").distinct().count()

    recent_diagnoses = Diagnosis.objects.filter(doctor=doctor).order_by("-created_at")[:5]

    weekly_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_visits_labels = [day.strftime("%a") for day in weekly_dates]
    weekly_visits_data = [
        Appointment.objects.filter(doctor=doctor, date=day).count()
        for day in weekly_dates
    ]

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
        "visited_count": visited_qs.count(),
        "not_visited_count": not_visited_qs.count(),
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

    today = timezone.now().date()

    appointments = Appointment.objects.filter(
        patient=user,
        date__gte=today,
        status__in=["PENDING", "CONFIRMED"]
    ).order_by("date", "time")

    diagnoses = Diagnosis.objects.filter(patient=user).order_by("-created_at")

    return render(request, 'dashboard/dashboard_patient.html', {
        'appointments': appointments,
        'diagnoses': diagnoses,
    })


# ===========================
# Visited Appointments
# ===========================
@login_required
def visited_patients(request):
    doctor = request.user.doctor
    now = timezone.now()

    visited = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).filter(
        Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time())
    ).select_related("patient").order_by("-date", "-time")

    not_visited = Appointment.objects.filter(
        doctor=doctor,
        status="CONFIRMED"
    ).exclude(id__in=visited.values_list("id", flat=True)).select_related("patient").order_by("date", "time")

    return render(request, "dashboard/visited_patients.html", {
        "visited_appointments": visited,
        "not_visited_appointments": not_visited,
    })


# ===========================
# Patient Detail View
# ===========================
@login_required
def patient_detail(request, patient_id):
    doctor = request.user.doctor
    patient = User.objects.get(id=patient_id)

    appointments = Appointment.objects.filter(doctor=doctor, patient=patient).order_by("-date", "-time")
    diagnoses = Diagnosis.objects.filter(doctor=doctor, patient=patient).order_by("-created_at")

    return render(request, "dashboard/patient_detail.html", {
        "patient": patient,
        "appointments": appointments,
        "diagnoses": diagnoses,
    })


# ===========================
# Reports Page (with Date Filter)
# ===========================
@login_required
def reports_page(request):
    doctor = request.user.doctor
    start = request.GET.get("start")
    end = request.GET.get("end")

    appointments = Appointment.objects.filter(doctor=doctor, status="CONFIRMED")

    if start:
        appointments = appointments.filter(date__gte=parse_date(start))
    if end:
        appointments = appointments.filter(date__lte=parse_date(end))

    return render(request, "dashboard/reports.html", {
        "appointments": appointments,
        "start": start,
        "end": end,
    })


# ===========================
# Download Patient-Specific PDF
# ===========================
@login_required
def download_patient_report(request, patient_id):
    doctor = request.user.doctor
    patient = User.objects.get(id=patient_id)

    appointments = Appointment.objects.filter(doctor=doctor, patient=patient, status="CONFIRMED")
    diagnoses = Diagnosis.objects.filter(doctor=doctor, patient=patient)

    template = get_template("dashboard/report_pdf_template.html")
    html = template.render({
        "doctor": doctor,
        "patient": patient,
        "appointments": appointments,
        "diagnoses": diagnoses,
    })

    response = HttpResponse(content_type="application/pdf")
    filename = f'{patient.get_full_name() or patient.username}_report.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed: %s' % pisa_status.err)
    return response


@login_required
@csrf_exempt
def mark_appointment_status(request, appointment_id):
    if request.method == "POST":
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if request.user != appointment.doctor.user:
                return redirect("dashboard:doctor_dashboard")

            status = request.POST.get("status")
            if status == "visited":
                # Mark past date and time
                appointment.date = timezone.now().date()
                appointment.time = timezone.now().time()
                appointment.status = "CONFIRMED"
                messages.success(request, "Marked as visited.")
            elif status == "not_visited":
                appointment.status = "CONFIRMED"  # still confirmed
                messages.info(request, "Marked as not visited.")
            appointment.save()
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
    return redirect("dashboard:doctor_dashboard")

