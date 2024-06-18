from rest_framework import serializers
from .models import Hospital, Patient, MedicalData, MedicalDataImages, DiagnosisReport, DiagnosisReportImages
from core.models import User

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'phone']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'hospital']

class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = ['id', 'patient', 'description', 'uploaded_at']

class MedicalDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDataImages
        fields = ['id', 'image', 'medical_data']

class DiagnosisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReport
        fields = ['id', 'medical_data', 'report', 'created_at']

class DiagnosisReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReportImages
        fields = ['id', 'image', 'diagnosis_report']
