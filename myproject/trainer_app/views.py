from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib import messages
from auth_app.models import BaseUser
from .models import TrainerProfile
from django.views.decorators.cache import never_cache
from attendance_app.models import Attendance
from student_app.models import StudentProfile

# trainer_app/views.py

@never_cache
def trainer_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        expertise = request.POST.get('expertise')
        email = request.POST.get('email')
        password = request.POST.get('password')
        token = request.POST.get('registration_token')

        try:
            trainer = TrainerProfile.objects.get(email=email, registration_token=token, user__isnull=True)
        except TrainerProfile.DoesNotExist:
            messages.error(request, "Invalid token or email, or account already activated.")
            return redirect('trainer_signup')

        if BaseUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('trainer_signup')

        # Create user and link to trainer profile
        user = BaseUser.objects.create_user(email=email, password=password, role='trainer')
        trainer.user = user
        trainer.full_name = full_name
        trainer.phone = phone
        trainer.expertise = expertise
        trainer.save()

        messages.success(request, "Trainer registered successfully. Please login.")
        return redirect('trainer_login')

    return render(request, 'trainer_app/signup.html')





@never_cache
def trainer_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'trainer':
        return redirect('trainer_login')

    trainer_profile = TrainerProfile.objects.get(user=request.user)
    batches = trainer_profile.batches.all()

    total_present = Attendance.objects.filter(trainer=trainer_profile, present=True).count()

    working_days = Attendance.objects.filter(batch__in=batches).values_list('date', flat=True).distinct()
    total_working_days = len(working_days)

 
    total_students = StudentProfile.objects.filter(batch__in=batches).distinct().count()


    expected_total = total_students * total_working_days
    total_absent = expected_total - total_present

    
    batch_attendance = []
    for batch in batches:
        student_count = batch.students.count()

        present = Attendance.objects.filter(batch=batch, trainer=trainer_profile, present=True).count()
        expected_batch_total = student_count * total_working_days
        absent = expected_batch_total - present

        batch_attendance.append({
            'batch_name': batch.name,
            'present': present,
            'absent': absent
        })

    return render(request, 'trainer_app/dashboard.html', {
        'trainer': trainer_profile,
        'total_present': total_present,
        'total_absent': total_absent,
        'batch_attendance': batch_attendance
    })


@never_cache
def trainer_qr_scanner(request):
    if not request.user.is_authenticated or request.user.role != 'trainer':
        return redirect('trainer_login')

    return render(request, 'trainer_app/qr_scanner.html')


@never_cache
def trainer_logout(request):
    logout(request)
    return redirect('homepage')
