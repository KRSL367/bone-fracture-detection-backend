from rest_framework import permissions
from .models import Hospital
from core.models import User  # Import the User model from core

class IsHospitalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the hospital from the URL
        hospital_pk = view.kwargs.get('hospital_pk')
        if not hospital_pk:
            return False

        # Check if the user is an admin of the hospital
        try:
            hospital = Hospital.objects.get(pk=hospital_pk)
            return request.user in hospital.admins.all()
        except Hospital.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin of the hospital
        try:
            return request.user in obj.hospital.admins.all()
        except AttributeError:
            return False
