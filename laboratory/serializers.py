from rest_framework import serializers
from .models import Patient, MedicalData, DiagnosisReport, Hospital, MedicalDataImages, DiagnosisReportImages

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'phone']
        read_only_fields = ['id']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'hospital']

class MedicalDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDataImages
        fields = ['id', 'image', 'medical_data']

class MedicalDataSerializer(serializers.ModelSerializer):
    images = MedicalDataImagesSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalData
        fields = ['id', 'patient', 'description', 'uploaded_at', 'images']

class DiagnosisReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReportImages
        fields = ['id', 'image', 'diagnosis_report']

class DiagnosisReportSerializer(serializers.ModelSerializer):
    diagnosis_images = DiagnosisReportImageSerializer(many=True, read_only=True)

    class Meta:
        model = DiagnosisReport
        fields = ['id', 'medical_data', 'report', 'created_at', 'diagnosis_images']
