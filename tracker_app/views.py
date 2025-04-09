from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from auth_app.models import BaseUser
from tracker_app.models import TrackerProfile, Batch
from attendance_app.models import Attendance
from django.shortcuts import render
from trainer_app.models import TrainerProfile
import csv
from collections import defaultdict
from django.http import HttpResponse
from attendance_app.models import Attendance
from trainer_app.models import TrainerProfile
from tracker_app.models import Batch

# tracker_app/views.py

@never_cache
def tracker_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        token = request.POST.get('registration_token')

        try:
            tracker = TrackerProfile.objects.get(email=email, registration_token=token, user__isnull=True)
        except TrackerProfile.DoesNotExist:
            messages.error(request, "Invalid token or email, or account already activated.")
            return redirect('tracker_signup')

        if BaseUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('tracker_signup')

        # Create user and link
        user = BaseUser.objects.create_user(email=email, password=password, role='tracker')
        tracker.user = user
        tracker.full_name = full_name
        tracker.save()

        messages.success(request, "Tracker registered successfully. Please login.")
        return redirect('tracker_login')

    return render(request, 'tracker_app/tracker_signup.html')



@never_cache
def tracker_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user and user.role == 'tracker':
            login(request, user)
            return redirect('tracker_dashboard')
        messages.error(request, "Invalid tracker credentials")
        return redirect('tracker_login')

    return render(request, 'tracker_app/tracker_login.html')



from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render


@never_cache
@login_required
def tracker_dashboard(request):
    search_query = request.GET.get('search', '').strip()
    print(f"[DEBUG] Search query received: '{search_query}'")

    batches = Batch.objects.filter(name__istartswith=search_query)
    print(f"[DEBUG] Matching batches count: {batches.count()}")
    if not batches.exists():
        print("[DEBUG] No batches matched. Available batch names:")
        for batch in Batch.objects.all():
            print(f" - {batch.name}")

    data = []
    for batch in batches:
        for trainer in batch.trainers.all():
            students = batch.students.filter(batch__trainers=trainer).distinct()
            student_list = []

            total_days = Attendance.objects.filter(
                batch=batch, trainer=trainer
            ).values_list('date', flat=True).distinct().count()

            for student in students:
                attendance_logs = Attendance.objects.filter(
                    student=student, trainer=trainer, batch=batch
                ).order_by('-date')

                present_days = attendance_logs.values('date').distinct().count()
                attendance_percentage = round((present_days / total_days) * 100) if total_days else 0

                student_list.append({
                    'student': student,
                    'attendance_logs': attendance_logs,
                    'attendance_percentage': attendance_percentage
                })

            data.append({
                'batch_id': batch.id,
                'batch_name': batch.name,
                'trainer': trainer,
                'students': student_list
            })

    return render(request, 'tracker_app/dashboard.html', {
        'batch_data': data,
        'search_query': search_query
    })



@never_cache
def export_csv(request, batch_name):
    import csv
    from collections import defaultdict
    from django.http import HttpResponse
    from attendance_app.models import Attendance
    from trainer_app.models import TrainerProfile
    from student_app.models import StudentProfile
    from tracker_app.models import Batch

    trainer_id = request.GET.get('trainer_id')

    try:
        batch = Batch.objects.get(name=batch_name)
    except Batch.DoesNotExist:
        return HttpResponse("Batch not found", status=404)

    trainer = None
    if trainer_id:
        try:
            trainer = TrainerProfile.objects.get(id=trainer_id)
        except TrainerProfile.DoesNotExist:
            return HttpResponse("Trainer not found", status=404)

    if trainer:
        attendances = Attendance.objects.filter(batch=batch, trainer=trainer).order_by('date')
    else:
        attendances = Attendance.objects.filter(batch=batch).order_by('date')

    unique_dates = sorted(set(att.date for att in attendances))
    enrolled_students = batch.students.all()

    
    student_data = {}
    for student in enrolled_students:
        student_data[student.full_name] = {
            'trainer': trainer.full_name if trainer else 'N/A',
            'status_by_date': {date: 'Absent' for date in unique_dates}
        }

    
    for att in attendances:
        if att.present and att.student.full_name in student_data:
            student_data[att.student.full_name]['status_by_date'][att.date] = 'Present'

   
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{batch_name}_{trainer.full_name if trainer else 'all'}_attendance.csv"'

    writer = csv.writer(response)

    
    header = ['Student Name', 'Trainer Name'] + [str(date) for date in unique_dates]
    writer.writerow(header)

   
    for student_name, data in student_data.items():
        row = [student_name, data['trainer']] + [data['status_by_date'][date] for date in unique_dates]
        writer.writerow(row)

    return response






@never_cache
def export_pdf(request, batch_name):
    trainer_id = request.GET.get('trainer_id')

    try:
        batch = Batch.objects.get(name=batch_name)
    except Batch.DoesNotExist:
        return HttpResponse("Batch not found", status=404)

    trainer = None
    if trainer_id:
        try:
            trainer = TrainerProfile.objects.get(id=trainer_id)
        except TrainerProfile.DoesNotExist:
            return HttpResponse("Trainer not found", status=404)

    enrolled_students = batch.students.all()


    if trainer:
        attendances = Attendance.objects.filter(batch=batch, trainer=trainer).order_by('date')
    else:
        attendances = Attendance.objects.filter(batch=batch).order_by('date')

    unique_dates = sorted(set(att.date for att in attendances))

    student_data = {}
    for student in enrolled_students:
        
        status_by_date = {date: 'Absent' for date in unique_dates}

       
        student_attendance = attendances.filter(student=student)

     
        for att in student_attendance:
            if att.present:
                status_by_date[att.date] = 'Present'

        student_data[student.full_name] = {
            'trainer': trainer.full_name if trainer else 'N/A',
            'status_by_date': status_by_date,
        }

    context = {
        'batch_name': batch_name,
        'trainer_name': trainer.full_name if trainer else "All Trainers",
        'unique_dates': unique_dates,
        'student_data': student_data,
    }

    template = get_template('tracker_app/attendance_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{batch_name}_{trainer.full_name if trainer else 'all'}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response
