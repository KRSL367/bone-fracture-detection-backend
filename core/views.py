# # core/views.py
# from djoser.views import UserViewSet as DjoserUserViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .serializers import UserCreateSerializer, UserSerializer
# from .models import User

# class UserViewSet(DjoserUserViewSet):
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         if self.action in ['create', 'update']:
#             return UserCreateSerializer
#         return UserSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser:
#             return User.objects.all()
#         elif user.is_hospital_admin:
#             return User.objects.filter(hospital=user.hospital)
#         return User.objects.none()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

import logging
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserSerializer
from .permissions import IsHospitalAdmin
from .models import User

logger = logging.getLogger(__name__)

class UserViewSet(DjoserUserViewSet):
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"User: {user.username}, is_superuser: {user.is_superuser}, is_hospital_admin: {user.is_hospital_admin}, hospital: {user.hospital}")
        
        if user.is_superuser:
            return User.objects.all()
        elif user.is_hospital_admin:
            hospital_users = User.objects.filter(hospital=user.hospital)
            logger.debug(f"Returning users for hospital: {user.hospital}")
            return hospital_users
        return User.objects.none()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserCreateSerializer
        return UserSerializer
