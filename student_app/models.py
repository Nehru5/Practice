from django.db import models
from auth_app.models import BaseUser
import uuid

class StudentProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, null=True, blank=True)  # User not linked initially
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Used to lookup during signup
    admission_date = models.DateField(auto_now_add=True)
    registration_token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_registered = models.BooleanField(default=False)  # To check if student already signed up

    def __str__(self):
        return self.full_name
