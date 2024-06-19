# from djoser.serializers import (
#     UserSerializer as BaseUserSerializer,
#     UserCreateSerializer as BaseUserCreateSerializer,
# )
# from rest_framework import serializers
# from .models import User
# from laboratory.models import Hospital

# class UserCreateSerializer(BaseUserCreateSerializer):
#     hospital_name = serializers.CharField(write_only=True, required=False)

#     class Meta(BaseUserCreateSerializer.Meta):
#         model = User
#         fields = ["id", "username", "password", "email", "first_name", "last_name", "hospital_name"]

#     def validate(self, attrs):
#         hospital_name = attrs.pop('hospital_name', None)
#         if hospital_name:
#             try:
#                 hospital = Hospital.objects.get(name=hospital_name)
#                 attrs['hospital'] = hospital
#             except Hospital.DoesNotExist:
#                 raise serializers.ValidationError(f"Hospital with name '{hospital_name}' does not exist.")
#         return super().validate(attrs)

# class UserSerializer(BaseUserSerializer):
#     hospital_name = serializers.CharField(source='hospital.name', read_only=True)

#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = ["id", "username", "email", "first_name", "last_name", "hospital_name"]

# core/serializers.py
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from .models import User
from laboratory.models import Hospital

class UserCreateSerializer(BaseUserCreateSerializer):
    hospital_name = serializers.CharField(write_only=True, required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name", "hospital_name"]

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
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "hospital_name"]





