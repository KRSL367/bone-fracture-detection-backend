from django.contrib import admin
from . import models 

admin.site.register(models.Hospital)
admin.site.register(models.Patient)
admin.site.register(models.MedicalData)
admin.site.register(models.DiagnosisReport)


