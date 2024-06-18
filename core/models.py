from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_hospital_admin = models.BooleanField(default=False)
    hospital = models.OneToOneField('laboratory.Hospital', related_name='admin', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
