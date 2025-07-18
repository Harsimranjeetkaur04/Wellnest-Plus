from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PatientSignUpForm, DoctorSignUpForm, DoctorProfileForm
from appointments.models import Appointment
from diagnosis.models import Diagnosis
from accounts.models import Doctor
from .forms import EmailAuthenticationForm



# ---------------------------
# Registration Views
# ---------------------------

def register_patient(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient registered successfully! Please log in.")
            return redirect('login')
    else:
        form = PatientSignUpForm()
    return render(request, 'accounts/register_patient.html', {'form': form})


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor registered successfully! Please log in.")
            return redirect('login')
    else:
        form = DoctorSignUpForm()
    return render(request, 'accounts/register_doctor.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ Role-based redirect using namespaced URLs
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
            elif user.is_superuser:
                return redirect('/admin/')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
8

# ---------------------------
# Dashboards
# ---------------------------

@login_required
def patient_dashboard(request):
    user = request.user
    appointments = Appointment.objects.filter(patient=user).order_by('-date')
    diagnoses = Diagnosis.objects.filter(patient=user).order_by('-created_at')

    return render(request, 'dashboard/dashboard_patient.html', {
        'appointments': appointments,
        'diagnoses': diagnoses,
    })


# @login_required
# def doctor_dashboard(request):
#     return render(request, 'dashboard/doctor_dashboard.html',context)


# ---------------------------
# Profile Views
# ---------------------------

@login_required
def user_profile(request):
    user = request.user

    if user.is_doctor:
        doctor = Doctor.objects.filter(user=user).first()
        return render(request, 'dashboard/profile.html', {
            'user': user,
            'doctor': doctor,
            'is_doctor': True
        })

    elif user.is_patient:
        return render(request, 'dashboard/patient_profile.html', {
            'user': user,
            'is_patient': True
        })

    return redirect('home')



@login_required
def edit_doctor_profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('profile')

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'accounts/edit_doctor_profile.html', {'form': form})


# ---------------------------
# Role-Based Redirect After Login (Fallback)
# ---------------------------

@login_required
def login_redirect(request):
    if request.user.is_doctor:
        return redirect('dashboard:doctor_dashboard')
    elif request.user.is_patient:
        return redirect('dashboard:patient_dashboard')
    else:
        return redirect('home')


# ---------------------------
# Home Page View
# ---------------------------

def home(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required
from .forms import PatientProfileForm

@login_required
def edit_patient_profile(request):
    if not request.user.is_patient:
        return redirect('home')

    user = request.user

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect('dashboard:patient_dashboard')
    else:
        form = PatientProfileForm(instance=user)

    return render(request, 'accounts/edit_patient_profile.html', {'form': form})

