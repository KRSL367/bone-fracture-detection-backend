from django.contrib import admin
from . import models 

# Register your models here.

admin.site.register(models.Patient)
admin.site.register(models.MedicalImage)
admin.site.register(models.Doctor)
admin.site.register(models.DiagnosisReport)
admin.site.register(models.Hospital)


