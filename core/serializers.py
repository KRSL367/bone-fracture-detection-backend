
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from laboratory.models import Hospital
from laboratory.serializers import HospitalSerializer
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    hospital_name = serializers.CharField(write_only=True, required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ["id","first_name", "last_name", "username",  "email", "password", "hospital_name"]

    def validate(self, attrs):
        request = self.context.get('request')
        hospital_name = attrs.pop('hospital_name')
        
        if request and request.user.is_hospital_admin:
            admin_hospital = request.user.hospital
            
            # Check if the hospital_name matches the admin's hospital
            if admin_hospital.name != hospital_name:
                raise serializers.ValidationError("You can only create users for your assigned hospital.")

        # Fetch the hospital based on the provided hospital_name
        try:
            hospital = Hospital.objects.get(name=hospital_name)
            attrs['hospital'] = hospital
        except Hospital.DoesNotExist:
            raise serializers.ValidationError(f"Hospital with name '{hospital_name}' does not exist.")
        
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

class UserSerializer(BaseUserSerializer):
    hospital = HospitalSerializer(read_only =True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ["id", "first_name", "last_name","username", "email", "hospital"]


class CustomTokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        refresh = RefreshToken.for_user(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.first_name + " " + user.last_name,
                "username": user.username,
                "is_hospital_admin": user.is_hospital_admin,
                "hospital_id": user.hospital_id,
                "is_superuser": user.is_superuser,
            },
        }

        return data


