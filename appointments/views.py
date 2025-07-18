from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'PENDING'
            appointment.save()
            messages.success(request, "Appointment request sent successfully.")
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.is_doctor:
        appointment.status = 'CONFIRMED'
        appointment.save()
    return redirect('doctor_dashboard')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.is_doctor:
        appointment.status = 'CANCELLED'
        appointment.save()
    return redirect('doctor_dashboard')



