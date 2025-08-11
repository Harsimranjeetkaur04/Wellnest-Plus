from django.urls import path
from . import views

urlpatterns = [
    path('patient_preview/<int:patient_id>/', views.patient_preview_api, name='patient_preview_api'),
    path("appointment-detail/<int:id>/", views.appointment_detail_api, name="appointment_detail_api"),

]
