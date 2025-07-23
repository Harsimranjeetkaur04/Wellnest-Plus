from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_doctor', 'is_patient', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    list_filter = ['is_doctor', 'is_patient', 'is_staff', 'is_superuser']

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('is_doctor', 'is_patient', 'profile_photo')
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree', 'available_days', 'contact']
    search_fields = ['user__username']

