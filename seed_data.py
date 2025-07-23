import os
import django
import random
from faker import Faker

from django.utils import timezone
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellnest_project.settings')  # 🔁 Replace with actual project name
django.setup()

from accounts.models import CustomUser, Doctor
from appointments.models import Appointment
from diagnosis.models import Diagnosis

fake = Faker()

# # 🚨 Delete existing non-superuser data (optional during dev)
# CustomUser.objects.filter(is_superuser=False).delete()
# Appointment.objects.all().delete()
# Diagnosis.objects.all().delete()

# Sample data
specializations = [
    "Cardiologist", "Neurologist", "Orthopedic", "Dermatologist",
    "General Physician", "ENT Specialist", "Psychiatrist", "Pediatrician"
]
degrees = ["MBBS", "MD", "MS", "DM", "MCh"]
diseases = ["Diabetes", "Hypertension", "Asthma", "Migraine", "Arthritis", "Flu", "Covid-19", "Bronchitis"]

# 📷 Random profile photo generator
def get_profile_photo(is_male):
    base = "https://randomuser.me/api/portraits/"
    gender = "men" if is_male else "women"
    return f"{base}{gender}/{random.randint(1, 80)}.jpg"

# 👤 Reusable user creator
def create_user(username_prefix, index, is_doctor=False, is_patient=False):
    is_male = random.choice([True, False])
    full_name = fake.name_male() if is_male else fake.name_female()
    first_name = full_name.split()[0]
    last_name = " ".join(full_name.split()[1:])
    username = f"{username_prefix}_{first_name.lower()}{index}"
    email = f"{username}@wellnest.com"

    new_user = CustomUser.objects.create_user(
        username=username,
        password="test1234",
        first_name=first_name,
        last_name=last_name,
        is_doctor=is_doctor,
        is_patient=is_patient,
        email=email,
        gender="M" if is_male else "F",
        age=random.randint(30, 60) if is_doctor else random.randint(18, 65),
        profile_photo=get_profile_photo(is_male),
    )
    return new_user, is_male

# 🧑‍⚕️ Create Doctors
doctors = []
for doctor_index in range(5):
    doctor_user, _ = create_user("dr", doctor_index, is_doctor=True)
    doctor = Doctor.objects.create(
        user=doctor_user,
        specialization=random.choice(specializations),
        degree=random.choice(degrees),
        available_days="Mon-Fri",
        availability_time="9am - 1pm",
        standard_fee=random.randint(300, 700),
        special_fee=random.randint(800, 1200),
        contact=fake.phone_number(),
        profile_photo=doctor_user.profile_photo
    )
    doctors.append(doctor)

# 🧍 Create Patients
patients = []
for patient_index in range(10):
    patient_user, _ = create_user("pat", patient_index, is_patient=True)
    patients.append(patient_user)

# 📅 Create Appointments
appointments = []
for _ in range(20):
    patient = random.choice(patients)
    doctor = random.choice(doctors)
    days_offset = random.randint(-5, 5)
    appt_datetime = timezone.now() + timedelta(days=days_offset)
    appt_time = appt_datetime.replace(hour=random.randint(9, 17), minute=0, second=0)

    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        date=appt_time.date(),
        time=appt_time.time(),
        status=random.choice(['confirmed', 'pending']),
        reason=fake.sentence(nb_words=6)
    )
    appointments.append(appointment)

# 🧾 Create Diagnoses
for _ in range(15):
    linked_appointment = random.choice(appointments)
    Diagnosis.objects.create(
        patient=linked_appointment.patient,
        doctor=linked_appointment.doctor,
        diagnosed_disease=random.choice(diseases),
        notes=fake.paragraph(nb_sentences=3),
        appointment=linked_appointment
    )

print("✅ Seeder script completed with realistic doctor/patient data.")
