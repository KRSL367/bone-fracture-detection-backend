from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenCreateSerializer, UserSerializer, UserCreateSerializer
from .permissions import IsHospitalAdmin
from .models import User

class UserViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_hospital_admin:
            hospital_users = User.objects.filter(hospital=user.hospital)
            return hospital_users
        else:
            return User.objects.filter(id=user.id)
        
class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer