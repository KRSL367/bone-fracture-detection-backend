from rest_framework import serializers
from .models import Patient, MedicalImage

class PatientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Patient
        fields = '__all__'

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = ['id', 'patient', 'image', 'uploaded_at', 'diagnosis']