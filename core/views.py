from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Patient, Report
from googletrans import Translator

def home(request):
    return HttpResponse("""
    <h1>Welcome to Hospital Portal</h1>
    <p>Access patient dashboard using: /patient/&lt;patient_id&gt;/</p>
    <p>Example: <a href="/patient/P001/">/patient/P001/</a></p>
    """)

def patient_portal(request, p_id):
    # Database se patient dhundo
    patient = get_object_or_404(Patient, p_id=p_id)
    
    # Language check karo (URL mein ?lang=hi hoga)
    lang = request.GET.get('lang', 'en')
    
    translator = Translator()

    # Translation Helper
    def translate(text):
        if lang == 'en': return text
        try:
            return translator.translate(str(text), dest=lang).text
        except:
            return text

    existing_reports = Report.objects.filter(patient=patient).order_by('-uploaded_at')

    # Data ready karo template ke liye
    context = {
        'patient': patient,
        'current_lang': lang,
        # Translated Fields
        't_status': translate(patient.status),
        't_disease': translate(patient.disease),
        't_next_test': translate(patient.next_test),
        't_note': translate(patient.doctor_note),
        't_name_label': translate("Patient Name"),
        't_status_label': translate("Current Status"),
        't_test_label': translate("Upcoming Test"),
        't_note_label': translate("Doctor's Message"),
        'existing_reports': existing_reports,
        'reviewer_doctor_name': patient.reviewer_doctor_name,
        't_plan_of_action': translate(patient.plan_of_action),
        't_procedure_planned': translate(patient.prcedure_planned),
        't_treatment_given': translate(patient.treatment_given),
        't_next_visit_planned': translate(patient.next_visit_panned),
        't_diagnosis': translate(patient.diagnosis),
    }
    
    return render(request, 'patient_dashboard.html', context)