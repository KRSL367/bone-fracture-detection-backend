# laboratory/permissions.py
from rest_framework import permissions
from .models import Hospital

class IsHospitalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        hospital_pk = view.kwargs.get('hospital_pk')
        if not hospital_pk:
            return False

        try:
            hospital = Hospital.objects.get(pk=hospital_pk)
            return request.user in hospital.admins.all()
        except Hospital.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return request.user in obj.hospital.admins.all()
        except AttributeError:
            return False
