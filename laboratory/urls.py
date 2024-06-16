# laboratory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    MedicalImageViewSet,
    DoctorViewSet,
    DiagnosisReportViewSet,
    HospitalViewSet,
)


router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("medical-images", MedicalImageViewSet, basename="medicalimage")
router.register("doctors", DoctorViewSet, basename="doctor")
router.register("diagnosis-reports", DiagnosisReportViewSet)
router.register("hospitals", HospitalViewSet, basename="hospital")

urlpatterns = [
    path("", include(router.urls)),
]
