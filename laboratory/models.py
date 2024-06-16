from django.db import models
from django.conf import settings 

class Patient(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class MedicalImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_images')
    image = models.ImageField(upload_to='medical_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image {self.id} for {self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

class DiagnosisReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medical_image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diagnosis Report for {self.patient} by {self.doctor} on {self.report_date}"

