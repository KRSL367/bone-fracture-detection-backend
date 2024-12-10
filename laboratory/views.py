from django.forms import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
import requests
from django.db import transaction

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
    
    
    @action(detail=False, methods=['post'], url_path='images-for-x-ray-check')
    def images_for_xray_check(self, request, *args, **kwargs):
        medical_id = request.data.get("medical_id")
        if not medical_id:
            return Response({"error": "Medical ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch images associated with the blood test ID
            images = MedicalDataImages.objects.filter(medical_data_id=medical_id)
            if not images.exists():
                return Response({"error": "No images found for the provided Medical ID"}, status=status.HTTP_404_NOT_FOUND)
        except MedicalDataImages.DoesNotExist:
            return Response({"error": "X-Ray test data not found"}, status=status.HTTP_404_NOT_FOUND)

        # Construct absolute URLs for the images
        image_urls = [request.build_absolute_uri(image.image.url) for image in images]

        # Prepare payload to send to FastAPI
        data = {
            "urls": image_urls
        }
        
        print(data)

        # URL of your FastAPI endpoints
        x_ray_api_url = 'http://127.0.0.1:7001/process_images/'

        try:
            # Send POST request to blood cell count FastAPI
            response_x_ray = requests.post(x_ray_api_url, json=data,  # Pass data as JSON
                headers={"Content-Type": "application/json"})
            response_x_ray.raise_for_status()
            response_x_ray_response = response_x_ray.json()

            # Extract results from the response
            x_ray = response_x_ray_response["results"]
            x_ray_detected = x_ray["detected"]  # List of detected conditions/features
            processed_images = x_ray["processed_image_urls"]  # List of processed image URLs

            # Ensure detected descriptions match the number of images
            if len(x_ray_detected) != len(processed_images):
                raise ValueError("Mismatch between detected features and processed image URLs.")

                    
            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Create a new DiagnosisReport instance
                diagnosis_report = DiagnosisReport.objects.create(
                    report="Diagnosed Image Results",
                    medical_data_id=medical_id
                )

                 # Save the processed image links and their corresponding descriptions
                for image_url, description in zip(processed_images, x_ray_detected):
                    DiagnosisReportImages.objects.create(
                        diagnosis_report=diagnosis_report,
                        image=image_url,
                        description=description  # Assuming a description field exists in the model
                    )
        
                return Response({"message": "Data stored successfully"}, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            error_message = f"Error sending images to FastAPI: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





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
