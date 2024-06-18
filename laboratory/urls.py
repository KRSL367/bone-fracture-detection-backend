from rest_framework_nested import routers
from .views import (
    HospitalViewSet, PatientViewSet, MedicalDataViewSet, 
    MedicalDataImagesViewSet, DiagnosisReportViewSet, DiagnosisReportImageViewSet
)

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
    "medical-images", MedicalDataImagesViewSet, basename="medical_data-images"
)
medical_data_router.register(
    "diagnosis-reports",
    DiagnosisReportViewSet,
    basename="medical-data-diagnosis-reports",
)

diagnosis_report_router = routers.NestedDefaultRouter(
    medical_data_router, "diagnosis-reports", lookup="diagnosis_report"
)
diagnosis_report_router.register(
    "diagnosis-images", DiagnosisReportImageViewSet, basename="diagnosis-report-images"
)

urlpatterns = router.urls + hospital_router.urls + patient_router.urls + medical_data_router.urls + diagnosis_report_router.urls
