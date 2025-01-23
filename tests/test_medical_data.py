from rest_framework import status
import pytest
from datetime import datetime
from model_bakery import baker


@pytest.fixture
def create_medical_data(api_client):
    def do_create_medical_data(medical_data, hospital_id, patient_id):
        url = f"/laboratory/hospitals/{hospital_id}/patients/{patient_id}/medical-datas/"
        return api_client.post(url, medical_data)

    return do_create_medical_data


@pytest.mark.django_db
class TestCreateMedicalData:
    def test_if_user_is_anonymous_returns_401(self, create_medical_data):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        medical_data = {
            "patient": patient.id,
            "description": "Detailed description of fractured part",
            "uploaded_at": datetime.now(),
        }

        # Act
        response = create_medical_data(medical_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, create_medical_data, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        medical_data = {
            "patient": patient.id,
            "description": "Detailed description of fractured part",
            "uploaded_at": datetime.now(),
        }

        # Act
        response = create_medical_data(medical_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, create_medical_data, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        medical_data = {
            "patient": "",
            "description": "",
            "uploaded_at": "",
        }

        # Act
        response = create_medical_data(medical_data, hospital.id, patient.id)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveMedicalData:
    def test_if_medical_data_exists_and_user_is_not_authenticated_returns_401(
        self, api_client, authenticate
    ):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        medical_data = baker.make("MedicalData", patient=patient)  # Create medical data for the patient

        # Act
        api_client.force_authenticate(user=None)
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/{medical_data.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_medical_data_exists_returns_200(self, api_client, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        medical_data = baker.make("MedicalData", patient=patient)  # Create medical data for the patient

        # Act
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/{medical_data.id}/"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_medical_data_does_not_exist_returns_404(self, api_client, authenticate):
        # Arrange
        hospital = baker.make("Hospital", id=1)  # Create a hospital with a specific ID
        authenticate(hospital_id=hospital.id)
        patient = baker.make("Patient", hospital=hospital)  # Create a patient associated with the hospital

        # Act
        response = api_client.get(
            f"/laboratory/hospitals/{hospital.id}/patients/{patient.id}/medical-datas/1/"
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
