from django.shortcuts import render, redirect
from django.contrib.auth import logout
from auth_app.models import BaseUser
from django.contrib import messages
import qrcode
import os
from django.conf import settings
from tracker_app.models import Batch
from admin_app.models import AdminProfile
from django.views.decorators.cache import never_cache
from student_app.models import StudentProfile
from trainer_app.models import TrainerProfile
from tracker_app.models import TrackerProfile

# @never_cache
# def admin_signup(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         full_name = request.POST.get('full_name')
#         phone = request.POST.get('phone')

#         if BaseUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered.")
#             return redirect('admin_signup')

#         user = BaseUser.objects.create_user(email=email, password=password, role='admin')
#         AdminProfile.objects.create(user=user, full_name=full_name, phone=phone)
#         messages.success(request, "Admin registered successfully. Please login.")
#         return redirect('admin_login')

#     return render(request, 'admin_app/signup.html')




@never_cache
def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('admin_login')
    
    batches = Batch.objects.all()
    return render(request, 'admin_app/dashboard.html', {'batches': batches})


# admin_app/views.py
from student_app.models import StudentProfile

from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from django.contrib import messages
from student_app.models import StudentProfile

import smtplib
from email.mime.text import MIMEText



@never_cache
def register_trainer_by_admin(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        expertise = request.POST.get('expertise')
        email = request.POST.get('email')

        # Check if already registered
        if TrainerProfile.objects.filter(email=email).exists():
            messages.error(request, "Trainer already registered.")
            return redirect('register_trainer_by_admin')

        # Create trainer profile
        trainer = TrainerProfile.objects.create(
            full_name=full_name,
            phone=phone,
            expertise=expertise,
            email=email
        )

        # Send Email
        sender = "Nehruraja9486@gmail.com"
        password = "milr gmmc ocim kqpe"
        receiver = email
        subject = "Your Trainer Registration Token"
        body = f"""
Hi {full_name},

Your trainer account has been created by the Admin.

Use the following registration token to complete your signup:
Registration Token: {trainer.registration_token}

Please use this token on the trainer signup page.

Thanks,
Admin
"""

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
            print(f"Email sent to {receiver}")
        except Exception as e:
            print(f"Email error: {e}")
        finally:
            server.quit()

        messages.success(request, f"Trainer registered. Token sent to {email}")
        return redirect('admin_dashboard')

    return render(request, 'admin_app/register_trainer.html')


@never_cache
def register_student_by_admin(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Check if already registered
        if StudentProfile.objects.filter(email=email).exists():
            messages.error(request, "Student already registered.")
            return redirect('register_student_by_admin')

        # Create student record
        student = StudentProfile.objects.create(
            full_name=full_name,
            phone=phone,
            email=email
        )

        # Prepare email
        sender = "Nehruraja9486@gmail.com"
        password = "milr gmmc ocim kqpe"
        receiver = email
        subject = "Your Account Registration Token"
        body = f"""
Hi {full_name},

Your student account has been created by the Admin.

Use the following registration token to complete your signup:
Registration Token: {student.registration_token}

Please use this token on the student signup page.

Thanks,
Admin
"""

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
            print(f"Message sent successfully to {receiver}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

        messages.success(request, f"Student registered. Token sent to {email}")
        return redirect('admin_dashboard')

    return render(request, 'admin_app/register_student.html')

@never_cache
def register_tracker_by_admin(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Check if already registered
        if TrackerProfile.objects.filter(email=email).exists():
            messages.error(request, "Tracker already registered.")
            return redirect('register_tracker_by_admin')

        # Create tracker profile
        tracker = TrackerProfile.objects.create(
            full_name=full_name,
            email=email
        )

        # Send Email with registration token
        sender = "Nehruraja9486@gmail.com"
        password = "milr gmmc ocim kqpe"
        receiver = email
        subject = "Your Tracker Registration Token"
        body = f"""
Hi {full_name},

Your tracker account has been created by the Admin.

Use the following registration token to complete your signup:
Registration Token: {tracker.registration_token}

Please use this token on the tracker signup page.

Thanks,
Admin
"""

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
            print(f"Email sent to {receiver}")
        except Exception as e:
            print(f"Email error: {e}")
        finally:
            server.quit()

        messages.success(request, f"Tracker registered. Token sent to {email}")
        return redirect('admin_dashboard')

    return render(request, 'admin_app/register_tracker.html')



@never_cache
def admin_logout(request):
    logout(request)
    return redirect('homepage')



@never_cache
def create_batch(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('admin_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        admin_profile = AdminProfile.objects.get(user=request.user)
 
        batch = Batch.objects.create(name=name, created_by=admin_profile)

        

        qr_data = f"{settings.NGROK_URL}/attendance/mark/{batch.qr_code_uuid}/"

        qr = qrcode.make(qr_data)

        qr_folder = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_folder, exist_ok=True)
        qr_filename = f"{batch.id}_qr.png"
        qr_path = os.path.join(qr_folder, qr_filename)

        qr.save(qr_path)

        return redirect('admin_dashboard')

    return render(request, 'admin_app/create_batch.html')



@never_cache
def add_users_to_batch(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('admin_login')

    batches = Batch.objects.all()
    students = StudentProfile.objects.all()
    trainers = TrainerProfile.objects.all()

    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        student_ids = request.POST.getlist('students')
        trainer_ids = request.POST.getlist('trainers')

        batch = Batch.objects.get(id=batch_id)

        for sid in student_ids:
            student = StudentProfile.objects.get(id=sid)
            batch.students.add(student)

        for tid in trainer_ids:
            trainer = TrainerProfile.objects.get(id=tid)
            batch.trainers.add(trainer)

        return redirect('admin_dashboard')

    return render(request, 'admin_app/add_users_to_batch.html', {
        'batches': batches,
        'students': students,
        'trainers': trainers
    })



