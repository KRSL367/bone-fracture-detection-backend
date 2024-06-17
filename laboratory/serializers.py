from rest_framework import serializers
from .models import Patient, MedicalData, DiagnosisReport, Hospital

class PatientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_data']

class MedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalData
        fields = ['id', 'patient', 'uploaded_at', 'diagnosis']

class DiagnosisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReport
        fields = ['id', 'patient', 'doctor', 'report_date', 'diagnosis', 'comments']

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id','name', 'phone']
        read_only_fields = ['id']