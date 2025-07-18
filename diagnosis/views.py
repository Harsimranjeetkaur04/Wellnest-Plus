from django.shortcuts import render, redirect, get_object_or_404
from diagnosis.utils import predict_condition
from records.models import SymptomRecord
from .forms import SymptomCheckForm  # make sure you import it
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DiagnosisCreateForm

@login_required
def symptom_checker_view(request):
    predicted = None

    if request.method == "POST":
        form = SymptomCheckForm(request.POST)
        if form.is_valid():
            symptoms_input = form.cleaned_data["symptoms"]
            predicted = predict_condition(symptoms_input)

            # Save the result
            SymptomRecord.objects.create(
                user=request.user,
                symptoms=symptoms_input,
                predicted_condition=predicted
            )
    else:
        form = SymptomCheckForm()

    # Fetch recent history
    history = SymptomRecord.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, "diagnosis/symptom_checker.html", {
        "form": form,
        "predicted": predicted,
        "history": history
    })

@login_required
def edit_symptom_record(request, record_id):
    record = get_object_or_404(SymptomRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        form = SymptomCheckForm(request.POST)
        if form.is_valid():
            new_symptoms = form.cleaned_data['symptoms']
            record.symptoms = new_symptoms
            record.predicted_condition = predict_condition(new_symptoms)
            record.save()
            return redirect('symptom_checker')
    else:
        form = SymptomCheckForm(initial={'symptoms': record.symptoms})

    return render(request, 'diagnosis/edit_record.html', {
        'form': form,
        'record': record
    })


@login_required
def delete_symptom_record(request, record_id):
    record = get_object_or_404(SymptomRecord, id=record_id, user=request.user)
    record.delete()
    return redirect('symptom_checker')


@login_required
def create_diagnosis(request):
    if not request.user.is_doctor:
        return redirect('home')

    if request.method == 'POST':
        form = DiagnosisCreateForm(request.POST)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.doctor = request.user.doctor  # Assuming 1:1 doctor-user link
            diagnosis.save()
            messages.success(request, "Diagnosis added successfully.")
            return redirect('doctor_dashboard')
    else:
        form = DiagnosisCreateForm()

    return render(request, 'diagnosis/create_diagnosis.html', {'form': form})

