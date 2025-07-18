import uuid
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Doctor
from django import forms


# -------------------------
# Base Sign-Up Form (Shared)
# -------------------------

class BaseSignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Email address'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Phone number'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Confirm password'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']


# -------------------------
# Patient Sign-Up Form
# -------------------------

class PatientSignUpForm(BaseSignUpForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Last Name'
        })
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Age',
            'min': '0'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Address',
            'rows': 3
        })
    )

    # 🆕 Additional Fields
    blood_group = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Blood Group (e.g. A+)'
        })
    )
    emergency_contact = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Emergency Contact Number'
        })
    )
    known_allergies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Known Allergies',
            'rows': 2
        })
    )
    existing_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Existing Medical Conditions',
            'rows': 2
        })
    )
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        base_username = self.cleaned_data['first_name']
        unique_suffix = str(uuid.uuid4())[:6]  # small random unique string
        user.username = f"{base_username}_{unique_suffix}"
        user.is_patient = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.age = self.cleaned_data['age']
        user.address = self.cleaned_data['address']
        user.blood_group = self.cleaned_data.get('blood_group', '')
        user.emergency_contact = self.cleaned_data.get('emergency_contact', '')
        user.known_allergies = self.cleaned_data.get('known_allergies', '')
        user.existing_conditions = self.cleaned_data.get('existing_conditions', '')
        user.profile_photo = self.cleaned_data.get('profile_photo')
        if commit:
            user.save()
        return user


# -------------------------
# Doctor Sign-Up Form
# -------------------------

class DoctorSignUpForm(BaseSignUpForm):
    specialization = forms.CharField(
        max_length=100,
        label="Specialization",
        widget=forms.TextInput(attrs={
            'placeholder': 'Specialization'
        })
    )
    profile_photo = forms.ImageField(
        required=False,
        label="Profile Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'w-full border-gray-300 rounded-md'})
    )

    degree = forms.CharField(
        max_length=100,
        label="Degree",
        widget=forms.TextInput(attrs={
            'placeholder': 'Degree'
        })
    )
    available_days = forms.CharField(
        max_length=100,
        label="Available Days (e.g. Mon-Fri)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Available Days'
        })
    )
    availability_time = forms.CharField(
        max_length=50,
        label="Availability Time (e.g. 10am - 2pm)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Availability Time'
        })
    )
    standard_fee = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        label="Standard Fee",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Standard Fee (₹)'
        })
    )
    special_fee = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        label="Special Appointment Fee",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Special Fee (₹)'
        })
    )
    contact = forms.CharField(
        max_length=100,
        label="Contact Info (Phone/Email)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Contact Info'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Re-enter Password"

        # Add Tailwind styling to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                degree=self.cleaned_data['degree'],
                available_days=self.cleaned_data['available_days'],
                availability_time=self.cleaned_data['availability_time'],
                standard_fee=self.cleaned_data['standard_fee'],
                special_fee=self.cleaned_data['special_fee'],
                contact=self.cleaned_data['contact'],
                profile_photo=self.cleaned_data.get('profile_photo')
            )
        return user


# -------------------------
# Doctor Profile Edit Form
# -------------------------

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'specialization',
            'degree',
            'available_days',
            'availability_time',
            'standard_fee',
            'special_fee',
            'contact',
            'profile_photo',
        ]
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-input'}),
            'degree': forms.TextInput(attrs={'class': 'form-input'}),
            'available_days': forms.TextInput(attrs={'class': 'form-input'}),
            'availability_time': forms.TextInput(attrs={'class': 'form-input'}),
            'standard_fee': forms.NumberInput(attrs={'class': 'form-input'}),
            'special_fee': forms.NumberInput(attrs={'class': 'form-input'}),
            'contact': forms.TextInput(attrs={'class': 'form-input'}),
        }


from django import forms
from django.contrib.auth import authenticate

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Email address',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
        'placeholder': 'Password',
    }))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            from accounts.models import CustomUser
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("❌ No account found with this email.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError("❌ Invalid email or password.")

            self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user

# -------------------------
# Patient Profile Edit Form
# -------------------------

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'gender', 'age', 'phone_number', 'address',
            'blood_group', 'emergency_contact', 'known_allergies', 'existing_conditions',
            'profile_photo'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'blood_group': forms.TextInput(attrs={'class': 'form-input'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'known_allergies': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'existing_conditions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
