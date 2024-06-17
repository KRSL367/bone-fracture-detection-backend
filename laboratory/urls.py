# laboratory/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    PatientViewSet,
    MedicalImageViewSet,
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

patient_router = routers.NestedDefaultRouter(hospital_router, "patients", lookup="patient")
patient_router.register("medical-images", MedicalImageViewSet, basename="patient-medical-images")

medical_image_router = routers.NestedDefaultRouter(patient_router, "medical-images", lookup="medical_image")
medical_image_router.register("diagnosis-reports", DiagnosisReportViewSet, basename="medical-image-diagnosis-reports")



urlpatterns = [
    path("", include(router.urls)),
    path("", include(hospital_router.urls)),
    path("", include(patient_router.urls)),
    path("", include(medical_image_router.urls)),
]
