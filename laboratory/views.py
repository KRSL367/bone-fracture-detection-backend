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
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, 
    Paragraph, 
    Spacer, 
    Table, 
    TableStyle, 
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
            # Fetch images associated with the medical_datas ID
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
    
    
    @action(detail=True, methods=["get"], url_path="generate-fractured-report")
    def generate_fractured_report(self, request, *args, **kwargs):
        diagnosis_id = request.query_params.get('diagnosis_id')
        
        if not diagnosis_id:
            return Response({"error": "diagnosis_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        hospital_id = self.kwargs.get("hospital_pk")
        return self.generate_pdf_response(hospital_id, diagnosis_id)

    def generate_pdf_response(self, hospital_id, diagnosis_id):
        hospital = get_object_or_404(Hospital, id=hospital_id)
        diagnosis_report = get_object_or_404(DiagnosisReport, id=diagnosis_id)
        medical_datas = diagnosis_report.medical_data
        patient = medical_datas.patient
        diagnosis_result_images = DiagnosisReportImages.objects.filter(diagnosis_report=diagnosis_report)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        style_header = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=24, alignment=1, spaceAfter=12)
        style_section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=20, spaceAfter=6)
        style_footer = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=14, alignment=1, spaceBefore=40)

        content = []

        # Header
        content.append(Paragraph(hospital.name, style_header))
        if hospital.phone:
            content.append(Paragraph(f"Phone: {hospital.phone}", styles['Normal']))
        content.append(Spacer(1, 12))

        # Patient Information
        content.append(Paragraph("Patient Information", style_section_heading))
        patient_info = [
            ["Name:", f"{patient.first_name} {patient.last_name}"],
            ["Email:", patient.email or "N/A"],
            ["Phone:", patient.phone or "N/A"],
            ["Birth Date:", patient.birth_date or "N/A"]
        ]
        table = Table(patient_info, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Test Details
        content.append(Paragraph("Test Details", style_section_heading))
        test_details = [
            ["Description:", medical_datas.description or "N/A"],
            ["Registered At:", medical_datas.uploaded_at.strftime("%Y-%m-%d %H:%M") if medical_datas.uploaded_at else "N/A"]
        ]
        table = Table(test_details, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Diagnosis Report
        content.append(Paragraph("Diagnosis Report", style_section_heading))
        report_summary = [["Summary:", diagnosis_report.report or "N/A"]]
        table = Table(report_summary, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Result Images
        content.append(Paragraph("Result Images", style_section_heading))
        if diagnosis_result_images.exists():
            image_table_data = []
            row = []
            for i, img in enumerate(diagnosis_result_images):
                img_file = img.image
                try:
                    if hasattr(img_file, 'read'):
                        image = Image(BytesIO(img_file.read()), width=2 * inch, height=2 * inch)
                    else:
                        image = Image(img_file.path, width=2 * inch, height=2 * inch)
                    row.append(image)
                    if len(row) == 3:
                        image_table_data.append(row)
                        row = []
                except Exception as e:
                    print(f"Error loading image: {e}")
            if row:
                image_table_data.append(row)

            image_table = Table(image_table_data, colWidths=[2 * inch] * 3)
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            content.append(image_table)

        # Footer
        content.append(Spacer(1, 12))
        content.append(Paragraph("End of Report", style_footer))

        doc.build(content)
        pdf_data = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{patient.first_name}_{patient.last_name}_report.pdf"'
        return response



class DiagnosisReportImageViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisReportImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DiagnosisReportImages.objects.filter(diagnosis_report_id=self.kwargs['diagnosis_report_pk'])
    
