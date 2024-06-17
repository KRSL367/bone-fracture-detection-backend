# views.py
from rest_framework import viewsets
from .models import Patient, MedicalData, DiagnosisReport, Hospital
from .serializers import (
    PatientSerializer,
    MedicalDataSerializer,
    DiagnosisReportSerializer,
    HospitalSerializer,
)


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(hospital_id=self.kwargs['hospital_pk'])

class MedicalDataViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalDataSerializer

    def get_queryset(self):
        return MedicalData.objects.filter(patient_id=self.kwargs['patient_pk'])


class DiagnosisReportViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportSerializer

    def get_queryset(self):
        return DiagnosisReport.objects.filter(medical_image_id=self.kwargs['medical_image_pk'])
