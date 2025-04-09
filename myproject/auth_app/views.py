from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache


def home(request):
    return render(request, "./auth_app/home.html")


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')
            return redirect('admin_login')

    return render(request, 'auth_app/admin_login.html')


def trainer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'trainer':
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'trainer_dashboard')
        else:
            messages.error(request, 'Invalid trainer credentials')
            return redirect('trainer_login')

    return render(request, 'auth_app/trainer_login.html')


def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'student':
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid student credentials')
            return redirect('student_login')

    return render(request, 'auth_app/student_login.html')

@never_cache
def user_logout(request):
    logout(request)
    return redirect('home')  
