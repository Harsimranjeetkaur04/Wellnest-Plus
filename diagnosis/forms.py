# diagnosis/forms.py
from django import forms
from .models import Diagnosis

class SymptomCheckForm(forms.Form):
    symptoms = forms.CharField(
        label="Describe your symptoms",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'e.g., fever, cough, body ache'
        }),
        help_text="Separate symptoms by commas or spaces"
    )

class DiagnosisCreateForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['patient', 'diagnosed_disease', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'diagnosed_disease': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Disease name'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
