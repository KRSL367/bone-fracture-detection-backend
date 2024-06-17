from django.contrib.auth.models import AbstractUser
from django.db import models
from laboratory.models import Hospital

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
        ('staff', 'Staff'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    hospital = models.ForeignKey(Hospital, related_name='users', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
