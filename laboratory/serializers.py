from rest_framework import serializers
from .models import Patient, MedicalImage, DiagnosisReport, Hospital

class PatientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = '__all__'

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = ['id', 'patient', 'image', 'uploaded_at', 'diagnosis']

class DiagnosisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReport
        fields = ['id', 'patient', 'doctor', 'medical_image', 'report_date', 'diagnosis', 'comments']

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'