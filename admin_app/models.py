from django.db import models
from auth_app.models import BaseUser

class AdminProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

