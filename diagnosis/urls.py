from django.urls import path

from . import views
from .views import symptom_checker_view, edit_symptom_record, delete_symptom_record

urlpatterns = [
    path('', symptom_checker_view, name='symptom_checker'),
    path('edit/<int:record_id>/', edit_symptom_record, name='edit_symptom_record'),
    path('delete/<int:record_id>/', delete_symptom_record, name='delete_symptom_record'),
    path('doctor/create/', views.create_diagnosis, name='create_diagnosis'),

]
