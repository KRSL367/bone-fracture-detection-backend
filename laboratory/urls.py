# laboratory/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    PatientViewSet,
    MedicalDataViewSet,
    DiagnosisReportViewSet,
    HospitalViewSet,
)

# router = DefaultRouter()
# router.register("patients", PatientViewSet, basename="patient")
# router.register("medical-images", MedicalImageViewSet, basename="medicalimage")
# router.register("diagnosis-reports", DiagnosisReportViewSet)
# router.register("hospitals", HospitalViewSet, basename="hospital")

router = routers.DefaultRouter()
router.register("hospitals", HospitalViewSet, basename="hospital")

hospital_router = routers.NestedDefaultRouter(router, "hospitals", lookup="hospital")
hospital_router.register("patients", PatientViewSet, basename="hospital-patients")

patient_router = routers.NestedDefaultRouter(
    hospital_router, "patients", lookup="patient"
)
patient_router.register(
    "medical-datas", MedicalDataViewSet, basename="patient-medical-data"
)

medical_data_router = routers.NestedDefaultRouter(
    patient_router, "medical-datas", lookup="medical_data"
)
medical_data_router.register(
    "diagnosis-reports",
    DiagnosisReportViewSet,
    basename="medical-data-diagnosis-reports",
)

urlpatterns = router.urls + hospital_router.urls + patient_router.urls + medical_data_router.urls 
