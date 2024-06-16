# laboratory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalImageViewSet, DoctorViewSet, DiagnosisReportViewSet


router = DefaultRouter()
# router.register(r'patients', PatientViewSet, basename='patient')
router.register('patients',PatientViewSet, basename='patient')
router.register('medical-images',MedicalImageViewSet, basename='medicalimage')
router.register('doctors',DoctorViewSet, basename='doctor')
router.register('diagnosis-reports',DiagnosisReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
