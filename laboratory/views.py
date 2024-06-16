# views.py
from rest_framework import viewsets
from .models import Patient, MedicalImage
from .serializers import PatientSerializer, MedicalImageSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
class MedicalImageViewSet(viewsets.ModelViewSet):
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer
