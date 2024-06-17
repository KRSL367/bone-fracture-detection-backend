from rest_framework import serializers
from .models import Patient, MedicalData, DiagnosisReport, Hospital, MedicalDataImages, DiagnosisReportImages

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id','name', 'phone']
        read_only_fields = ['id']

class PatientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'hospital']

class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = ['id', 'patient', 'uploaded_at', 'diagnosis']

class MedicalDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDataImages
        fields = ['id', 'image', 'medical_data']

class DiagnosisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReport
        fields = ['id', 'patient', 'doctor', 'report_date', 'diagnosis', 'comments']

class DiagnosisReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReportImages
        fields = ['id', 'image', 'diagnosis_report']

