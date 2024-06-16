# views.py
from rest_framework import viewsets
from .models import Patient, MedicalImage, Doctor, DiagnosisReport
from .serializers import PatientSerializer, MedicalImageSerializer, DoctorSerializer, DiagnosisReportSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
class MedicalImageViewSet(viewsets.ModelViewSet):
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DiagnosisReportViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisReport.objects.all()
    serializer_class = DiagnosisReportSerializer