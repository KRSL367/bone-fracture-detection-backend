# core/views.py
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated

class UserViewSet(DjoserUserViewSet):
    permission_classes = [IsAuthenticated]
