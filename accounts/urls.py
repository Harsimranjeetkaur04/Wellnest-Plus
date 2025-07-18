# accounts/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import register_doctor, home, edit_doctor_profile, edit_patient_profile
from dashboard import views as dashboard_views


urlpatterns = [
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', dashboard_views.doctor_dashboard, name='doctor_dashboard'),
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('profile/', views.user_profile, name='profile'),
    path('', home, name='home'),
    path('profile/edit/', edit_doctor_profile, name='edit_doctor_profile'),
    path('edit/patient/', edit_patient_profile, name='edit_patient_profile'),

]
