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
    permission_classes = [IsAuthenticated, IsHospitalAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_hospital_admin:
            hospital_users = User.objects.filter(hospital=user.hospital)
            return hospital_users
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        
class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer