from rest_framework import status
import pytest
from datetime import datetime
from model_bakery import baker


@pytest.fixture
def create_diagnosis_report(api_client):
    def do_create_diagnosis_report(
        diagnosis_report_data, hospital_id, patient_id, medical_data_id
    ):
        url = f"/laboratory/hospitals/{hospital_id}/patients/{patient_id}/medical-datas/{medical_data_id}/diagnosis-reports/"
        return api_client.post(url, diagnosis_report_data)

    return do_create_diagnosis_report


@pytest.mark.django_db
class TestCreateDiagnosisReports:
    def test_if_user_is_anonymous_returns_401(
        self, create_diagnosis_report, authenticate, api_client
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient

        diagnosis_report_data = {
            "report": "Detailed description of the fractured part",
            "medical_data": medical_data.id,
            "created_at": datetime.now(),
        }

        api_client.force_authenticate(user=None)

        # Act
        response = create_diagnosis_report(
            diagnosis_report_data,
            hospital.id,
            patient.id,
            medical_data.id,
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, create_diagnosis_report, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient

        diagnosis_report_data = {
            "report": "Detailed description of the fractured part",
            "medical_data": medical_data.id,
            "created_at": datetime.now(),
        }

        # Act
        response = create_diagnosis_report(
            diagnosis_report_data,
            hospital.id,
            patient.id,
            medical_data.id,
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(
        self, create_diagnosis_report, authenticate
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient

        diagnosis_report_data = {
            "report": "",
            "medical_data": medical_data.id,
        }

        # Act
        response = create_diagnosis_report(
            diagnosis_report_data,
            hospital.id,
            patient.id,
            medical_data.id,
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveDiagnosisReports:
    def test_if_diagnosis_reports_exist_and_user_is_not_authenticated_returns_401(
        self, api_client, authenticate
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient
        diagnosis_report = baker.make(
            "DiagnosisReport", medical_data=medical_data
        )  # Create a diagnosis report associated with the medical data

        # Act
        api_client.force_authenticate(user=None)
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/{medical_data.id}/diagnosis-reports/{diagnosis_report.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_diagnosis_reports_exist_and_user_is_authenticated_returns_200(
        self, api_client, authenticate
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient
        diagnosis_report = baker.make(
            "DiagnosisReport", medical_data=medical_data
        )  # Create a diagnosis report associated with the medical data

        # Act
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/{medical_data.id}/diagnosis-reports/{diagnosis_report.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_diagnosis_reports_do_not_exist_returns_404(
        self, api_client, authenticate
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)

        patient = baker.make(
            "Patient", hospital=hospital
        )  # Create a patient associated with the hospital
        medical_data = baker.make(
            "MedicalData", patient=patient
        )  # Create medical data for the patient

        # Act
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/{medical_data.id}/diagnosis-reports/1/"
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
