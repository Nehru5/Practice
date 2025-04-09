from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.conf import settings
from .models import StudentProfile
from auth_app.models import BaseUser
from attendance_app.models import Attendance
import qrcode
import os
from django.core.paginator import Paginator




@never_cache
def student_signup(request):
    if request.method == 'POST':
        registration_token = request.POST.get('registration_token')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = StudentProfile.objects.get(email=email, registration_token=registration_token, is_registered=False)
        except StudentProfile.DoesNotExist:
            messages.error(request, "Invalid registration token or email.")
            return redirect('student_signup')

        
        user = BaseUser.objects.create_user(email=email, password=password, role='student')
        student.user = user
        student.full_name = full_name
        student.phone = phone
        student.is_registered = True
        student.save()

        messages.success(request, "Student registered successfully. Please login.")
        return redirect('student_login')

    return render(request, 'student_app/signup.html')

from django.core.paginator import Paginator

@never_cache
def student_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect('student_login')

    student = StudentProfile.objects.get(user=request.user)
    batches = student.batch.all()
    qr_codes = []
    attendance_data = []
    total_present = total_absent = 0

    for batch in batches:
        trainer = batch.trainers.first()
        if not trainer:
            continue

        qr_data = f"{settings.RENDER_URL}/attendance/mark/{student.id}/{batch.qr_code_uuid}/{trainer.id}/"
        qr_filename = f"student_{student.id}_batch_{batch.id}_qr.png"
        qr_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', qr_filename)

        if not os.path.exists(qr_path):
            os.makedirs(os.path.dirname(qr_path), exist_ok=True)
            qr = qrcode.make(qr_data)
            qr.save(qr_path)

        qr_codes.append({
            'batch_name': batch.name,
            'trainer_name': trainer.full_name,
            'qr_image': f"/media/qr_codes/{qr_filename}"
        })

        presents = Attendance.objects.filter(student=student, batch=batch).count()
        working_days = Attendance.objects.filter(batch=batch).values_list('date', flat=True).distinct()
        absents = len(working_days) - presents

        total_present += presents
        total_absent += absents

        attendance_data.append({
            'batch_name': batch.name,
            'trainer_name': trainer.full_name,
            'present': presents,
            'absent': absents
        })

    # Pagination for QR Codes (4 per page)
    paginator = Paginator(qr_codes, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_app/dashboard.html', {
        'student': student,
        'page_obj': page_obj,
        'attendance_data': attendance_data,
        'total_present': total_present,
        'total_absent': total_absent,
    })


@never_cache
def student_logout(request):
    logout(request)
    return redirect('homepage')
