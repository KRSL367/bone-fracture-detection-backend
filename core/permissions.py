# # laboratory/permissions.py
# from rest_framework import permissions
# from laboratory.models import Hospital

# class IsHospitalAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the requesting user is authenticated
#         if request.user.is_authenticated:
#             # Check if the requesting user is a superuser
#             if request.user.is_superuser:
#                 return True
#             # Check if the requesting user is a hospital admin
#             elif hasattr(request.user, 'is_hospital_admin') and request.user.is_hospital_admin:
#                 # If the user is a hospital admin, ensure they can only create users for their own hospital
#                 hospital_id = request.user.hospital_id
#                 if 'hospital' in request.data:
#                     # If the request includes a hospital field, ensure it matches the admin's hospital
#                     return str(request.data['hospital']) == str(hospital_id)
#                 else:
#                     # If no hospital field is provided, default to the admin's hospital
#                     return True
#         # If the user is not authenticated or is not a hospital admin, deny permission
#         return False

# core/permissions.py
from rest_framework import permissions

class IsHospitalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the requesting user is authenticated
        if not request.user.is_authenticated:
            return False

        # Superuser has full access
        if request.user.is_superuser:
            return True

        # Check if the requesting user is a hospital admin
        if request.user.is_hospital_admin:
            return True

        # Regular users can only view their own data
        if view.action == 'retrieve' and request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Superuser has full access
        if request.user.is_superuser:
            return True

        # Check if the requesting user is a hospital admin and the object belongs to their hospital
        if request.user.is_hospital_admin:
            if hasattr(obj, 'hospital') and obj.hospital == request.user.hospital:
                return True
            if hasattr(obj, 'hospital_id') and obj.hospital_id == request.user.hospital_id:
                return True

        # Regular users can only view their own data
        if hasattr(obj, 'id') and obj.id == request.user.id:
            return True

        return False
