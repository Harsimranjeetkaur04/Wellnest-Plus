from django.contrib import admin
from .models import SymptomRecord

@admin.register(SymptomRecord)
class SymptomRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_condition', 'created_at')
    search_fields = ('user__username', 'predicted_condition')
