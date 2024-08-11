from django_filters.rest_framework import FilterSet
from .models import Patient, MedicalData, DiagnosisReport

class PatientFilter(FilterSet):
    class Meta:
        model = Patient
        fields = {
            'birth_date': ['lt', 'gt'],
            'hospital_name': ['exact'],
        }

class MedicalDataFilter(FilterSet):
    class Meta:
        model = MedicalData
        fields = {
            'date_recorded': ['lt', 'gt'],
            'patient': ['exact'],
        }

class DiagnosisReportFilter(FilterSet):
    class Meta:
        model = DiagnosisReport
        fields = {
            'diagnosis_date': ['lt', 'gt'],
            'patient': ['exact'],
            'report_type': ['exact'],
        }
