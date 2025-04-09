from django.db import models
from auth_app.models import BaseUser

# trainer_app/models.py
import uuid

class TrainerProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    expertise = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    registration_token = models.CharField(max_length=100, default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.full_name
