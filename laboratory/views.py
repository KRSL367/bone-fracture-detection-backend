# views.py
from rest_framework import viewsets
from .models import Patient, MedicalImage, DiagnosisReport, Hospital
from .serializers import (
    PatientSerializer,
    MedicalImageSerializer,
    DiagnosisReportSerializer,
    HospitalSerializer,
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class MedicalImageViewSet(viewsets.ModelViewSet):
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer

class DiagnosisReportViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisReport.objects.all()
    serializer_class = DiagnosisReportSerializer

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
