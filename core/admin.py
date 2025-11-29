from django.contrib import admin
from .models import Patient, Report

# Custom Admin Header
admin.site.site_header = "🏥 MediConnect Doctor Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Patient Management System"

class ReportInline(admin.TabularInline):
    model = Report
    extra = 1
    readonly_fields = ('uploaded_at',)
    fields = ('file', 'description', 'uploaded_at')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'p_id', 'age', 'status', 'admission_date', 'reviewer_doctor_name', 'plan_of_action')
    search_fields = ('name', 'p_id')
    fields = (
        'name', 'p_id', 'age', 'status', 'disease', 'next_test', 'doctor_note',
        'plan_of_action', 'reviewer_doctor_name', 'prcedure_planned', 'qr_code',
        'treatment_given', 'next_visit_panned','diagnosis',
    )
    inlines = [ReportInline]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'file', 'description', 'uploaded_at')
    search_fields = ('patient__p_id', 'description')