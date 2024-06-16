from rest_framework import serializers
from .models import Patient, MedicalImage, Doctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = '__all__'

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = ['id', 'patient', 'image', 'uploaded_at', 'diagnosis']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'specialization']
