from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from laboratory.models import Hospital


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=True, is_superuser=False, hospital_id=None):
        user = User.objects.create_user(username="testuser", password="testpass")
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        if hasattr(user, "hospital_id"):
            user.hospital_id = hospital_id
        user.save()
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


@pytest.fixture
def create_hospital_data():
    def do_create_hospital(hospital_id):
        return Hospital.objects.create(id=hospital_id, name="Test Hospital")

    return do_create_hospital


@pytest.fixture
def hospital_authenticate(api_client, create_hospital_data):
    def do_authenticate(is_staff=True, is_superuser=False, hospital_id=None):
        hospital = create_hospital_data(hospital_id)
        user = User.objects.create_user(
            username="testuser", password="testpass", hospital=hospital
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate
