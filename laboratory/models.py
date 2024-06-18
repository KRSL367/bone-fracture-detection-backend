from django.db import models
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

class MedicalData(models.Model):
    patient = models.ForeignKey(Patient, related_name='medical_datas', on_delete=models.CASCADE)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data {self.id} for {self.patient}"

class MedicalDataImages(models.Model):
    image = models.ImageField(upload_to='medical_images/')
    medical_data = models.ForeignKey(MedicalData, related_name='images', on_delete=models.CASCADE)

class DiagnosisReport(models.Model):
    medical_data = models.OneToOneField(MedicalData, related_name='diagnosis_report', on_delete=models.CASCADE)
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} for {self.medical_data}"

class DiagnosisReportImages(models.Model):
    image = models.ImageField(upload_to='report_images/')
    diagnosis_report = models.ForeignKey(DiagnosisReport, related_name='diagnosis_images', on_delete=models.CASCADE)
