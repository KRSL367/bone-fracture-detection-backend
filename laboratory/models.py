from django.db import models

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

