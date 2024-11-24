from rest_framework import serializers
from .models import Hospital, Patient, MedicalData, MedicalDataImages, DiagnosisReport, DiagnosisReportImages
from core.models import User

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'phone']

class MedicalDataImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDataImages
        fields = ['id', 'image', 'medical_data']

class DiagnosisReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReportImages
        fields = ['id', 'image', 'diagnosis_report']
        
class DiagnosisReportSerializer(serializers.ModelSerializer):
    diagnosis_images = DiagnosisReportImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = DiagnosisReport
        fields = ['id', 'medical_data', 'report', 'created_at', 'diagnosis_images']

class MedicalDataSerializer(serializers.ModelSerializer):
    images = MedicalDataImagesSerializer(many=True, read_only=True)
    diagnosis_report = DiagnosisReportSerializer(read_only = True, many = True)
    
    class Meta:
        model = MedicalData
        fields = ['id', 'patient', 'description', 'uploaded_at', 'images', 'diagnosis_report']

class PatientSerializer(serializers.ModelSerializer):
    medical_datas = MedicalDataSerializer(many=True, read_only=True)
    hospital = HospitalSerializer
    
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'medical_datas', 'hospital']
