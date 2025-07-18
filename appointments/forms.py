from django import forms
from .models import Appointment
from accounts.models import Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border-gray-300 rounded-md'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border-gray-300 rounded-md'}),
            'reason': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-md', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
