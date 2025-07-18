from django.urls import path
from . import views

app_name = 'dashboard'
from dashboard import views as dashboard_views

urlpatterns = [
    path('dashboard/doctor/', dashboard_views.doctor_dashboard, name='doctor_dashboard'), # ✅ correct

    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
]
