from django_filters.rest_framework import FilterSet
from .models import Patient, MedicalData, DiagnosisReport

class PatientFilter(FilterSet):
    class Meta:
        model = Patient
        fields = {
            'birth_date': ['lt', 'gt'],
            'hospital': ['exact'],
        }

class MedicalDataFilter(FilterSet):
    class Meta:
        model = MedicalData
        fields = {
            'uploaded_at': ['lt', 'gt'],
            "patient_id": ["exact"],
        }

class DiagnosisReportFilter(FilterSet):
    class Meta:
        model = DiagnosisReport
        fields = {
            'created_at': ['lt', 'gt'],
            "medical_data_id": ["exact"],
        }
