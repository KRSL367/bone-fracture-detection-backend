# laboratory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalImageViewSet  # Ensure correct import


router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'medical-images', MedicalImageViewSet, basename='med-image')



urlpatterns = [
    path('', include(router.urls)),
]
