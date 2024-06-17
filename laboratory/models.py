from django.db import models
from django.conf import settings 
from uuid import uuid4

class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    hospital = models.ForeignKey(Hospital, related_name='patients', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class MedicalImage(models.Model):
    patient = models.ForeignKey(Patient, related_name='medical_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='medical_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} for {self.patient}"

class DiagnosisReport(models.Model):
    medical_image = models.OneToOneField(MedicalImage, related_name='diagnosis_report', on_delete=models.CASCADE)
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='diagnosis_reports', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Report {self.id} for {self.medical_image}"

