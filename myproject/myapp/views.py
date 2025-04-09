from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import UserData

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def Signup(request):
  if request.method == "POST":
    a = request.POST.get("username")
    b = request.POST.get("password")
    hashed = make_password(b)
    
    UserData.objects.create(
      username = a,
      password = hashed
    )
    return redirect("login")
  return render(request,"signup.html")

def Login_(request):
    if request.method == "POST":
        a = request.POST.get("username")
        b = request.POST.get("password")
        
        user = UserData.objects.filter(username=a).first()
        username = user.username
        password = user.password
        if username == a and check_password(b, password):
          return HttpResponse("Logged in")
        else:
          return HttpResponse("Invalid credentials")
        
    
    
    return render(request, "login.html")
  
  
"""Session in Django"""


def Session_Example(request):
  request.session["username"] = "Nehru"
  request.session["stream"] = "ECE"
  return HttpResponse("Stored Successfully!!")

def Session_Get(request):
  username = request.session.get("username","Guest")
  stream = request.session.get("stream")
  request.session.set_expiry(0)
  
  return HttpResponse(f"Name: {username}\n Stream: {stream}")
  
def Flush(request):
  if "username" in request.session:
    request.session.flush()
    return HttpResponse("Session Cleared")
  else:
    return HttpResponse("No data in session")
  

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)