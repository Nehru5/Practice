from django.db import models
from student_app.models import StudentProfile
from trainer_app.models import TrainerProfile
from tracker_app.models import Batch

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {'Present' if self.present else 'Absent'}"
