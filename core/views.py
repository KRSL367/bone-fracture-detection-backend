# # core/views.py
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserSerializer
from .permissions import IsHospitalAdmin
from .models import User


class UserViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_queryset(self):
        user = self.request.user        
        if user.is_superuser:
            return User.objects.all()
        elif user.is_hospital_admin:
            hospital_users = User.objects.filter(hospital=user.hospital)
            return hospital_users
        return User.objects.filter(id = user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserCreateSerializer
        return UserSerializer
