# diagnosis/admin.py
from django.contrib import admin
from .models import Diagnosis

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosed_disease', 'appointment','symptoms')
