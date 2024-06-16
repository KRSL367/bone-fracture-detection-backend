from django.contrib.auth.models import AbstractUser
from django.db import models
from laboratory.models import Hospital

class User(AbstractUser):
    email = models.EmailField(unique=True)
    hospital_id = models.OneToOneField(Hospital, null=True, blank=True, on_delete=models.SET_NULL)
