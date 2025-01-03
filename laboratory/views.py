from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from laboratory.pagination import DefaultPagination
from .models import Patient, MedicalData, DiagnosisReport, Hospital, MedicalDataImages, DiagnosisReportImages
from .serializers import (
    PatientSerializer,
    MedicalDataSerializer,
    DiagnosisReportSerializer,
    HospitalSerializer,
    MedicalDataImagesSerializer,
    DiagnosisReportImageSerializer
)
from .filters import DiagnosisReportFilter,MedicalDataFilter,PatientFilter

class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = ['name']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Hospital.objects.all()
        elif user.is_hospital_admin:
            hospital = Hospital.objects.filter(name=user.hospital)
            return hospital
        else:
            return Hospital.objects.filter(name=user.hospital)

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = PatientFilter
    search_fields = ["first_name", "last_name", "phone", "email"]
    ordering_fields = ["first_name"]
 

    def get_queryset(self):
        return Patient.objects.filter(hospital_id=self.kwargs['hospital_pk'])

class MedicalDataViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicalDataFilter
    search_fields = ["description"]
    ordering_fields = ["uploaded_at"]

    def get_queryset(self):
        return MedicalData.objects.filter(patient_id=self.kwargs['patient_pk'])

class MedicalDataImagesViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalDataImagesSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return MedicalDataImages.objects.filter(medical_data_id=self.kwargs['medical_data_pk'])
    
    def create(self, request, *args, **kwargs):
        # Expecting files in request.FILES
        files = request.FILES.getlist("image")
        medical_data_id = self.kwargs["medical_data_pk"]
        data = [{"image": file, "medical_data": medical_data_id} for file in files]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["post"], url_path="batch-delete")
    def batch_delete(self, request, *args, **kwargs):
        # Collect all image_ids from the request data
        image_ids = request.data.getlist("image_ids")
        if not image_ids:
            return Response(
                {"error": "No image IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        images = MedicalDataImages.objects.filter(id__in=image_ids)
        count, _ = images.delete()
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)


class DiagnosisReportViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,
        OrderingFilter,DjangoFilterBackend]
    filterset_class = DiagnosisReportFilter
    search_fields = ["report"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return DiagnosisReport.objects.filter(medical_data_id=self.kwargs['medical_data_pk'])

class DiagnosisReportImageViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiagnosisReportImages.objects.filter(diagnosis_report_id=self.kwargs['diagnosis_report_pk'])
