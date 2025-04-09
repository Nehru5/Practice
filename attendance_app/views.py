from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from student_app.models import StudentProfile
from trainer_app.models import TrainerProfile
from attendance_app.models import Attendance, Batch
from django.utils import timezone


def mark_attendance(request, student_id, batch_uuid, trainer_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    batch = get_object_or_404(Batch, qr_code_uuid=batch_uuid)

    if batch not in student.batch.all():
        messages.error(request, "This student is not part of the scanned batch.")
        return redirect('student_login')

    
    if not request.user.is_authenticated or request.user.role != 'trainer':
        logout(request)
        messages.info(request, "Please login as a trainer to mark attendance.")
        return redirect('trainer_login')

    logged_trainer = TrainerProfile.objects.get(user=request.user)

    
    if logged_trainer.id != trainer_id:
        logout(request)
        messages.error(request, "Invalid trainer for this QR. Please login with the correct account.")
        return redirect('trainer_login')

    
    if logged_trainer not in batch.trainers.all():
        logout(request)
        messages.error(request, "You're not authorized to mark attendance for this batch.")
        return redirect('trainer_login')

    today = timezone.now().date()
   

    already_marked = Attendance.objects.filter(student=student, batch=batch, date=today).exists()

    if already_marked:
        messages.info(request, "Attendance already marked today.")
        return render(request, 'attendance_app/attendance_already_marked.html', {
            'student': student,
            'batch': batch
        })

    Attendance.objects.create(
        student=student,
        trainer=logged_trainer,
        batch=batch,
        date=today
    )
    messages.success(request, "Attendance marked successfully.")
    return render(request, 'attendance_app/attendance_success.html', {
        'student': student,
        'batch': batch
    })
