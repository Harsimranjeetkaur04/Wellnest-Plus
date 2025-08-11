from django.urls import path
from . import views

app_name = 'dashboard'
from dashboard import views as dashboard_views

urlpatterns = [
    path('dashboard/doctor/', dashboard_views.doctor_dashboard, name='doctor_dashboard'), # ✅ correct

    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('patient-records/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('visited-patients/', views.visited_patients, name='visited_patients'),
    path('reports/', views.reports_page, name='reports_page'),
    path('reports/download/<int:patient_id>/', views.download_patient_report, name='download_patient_report'),

]
