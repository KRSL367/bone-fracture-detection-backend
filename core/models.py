from django.contrib.auth.models import AbstractUser
from django.db import models
from laboratory.models import Hospital

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_hospital_admin = models.BooleanField(default=False)
    hospital = models.OneToOneField(Hospital, related_name='users', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
