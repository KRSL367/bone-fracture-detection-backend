# views.py
from rest_framework import viewsets
from .models import Patient, MedicalData, DiagnosisReport, Hospital, MedicalDataImages, DiagnosisReportImages
from .serializers import (
    PatientSerializer,
    MedicalDataSerializer,
    DiagnosisReportSerializer,
    HospitalSerializer,
    MedicalDataImagesSerializer,
    DiagnosisReportImageSerializer
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

class MedicalDataImagesViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalDataImagesSerializer

    def get_queryset(self):
        return MedicalDataImages.objects.filter(medical_data_id=self.kwargs['medical_data_pk'])

class DiagnosisReportViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportSerializer

    def get_queryset(self):
        return DiagnosisReport.objects.filter(medical_image_id=self.kwargs['medical_image_pk'])


class DiagnosisReportImageViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportImageSerializer

    def get_queryset(self):
        return DiagnosisReportImages.objects.filter(diagnosis_report_id=self.kwargs['diagnosis_report_pk'])