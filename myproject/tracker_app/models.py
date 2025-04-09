import uuid
from django.db import models
from django.conf import settings
from admin_app.models import AdminProfile
from trainer_app.models import TrainerProfile
from student_app.models import StudentProfile

User = settings.AUTH_USER_MODEL

# tracker_app/models.py

import uuid

class TrackerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_token = models.CharField(max_length=100, default=uuid.uuid4)

    def __str__(self):
        return self.full_name



class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    trainers = models.ManyToManyField(TrainerProfile, related_name='batches')
    students = models.ManyToManyField(StudentProfile, related_name='batch', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name
