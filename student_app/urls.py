from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.student_signup, name='student_signup'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.student_logout, name='student_logout'),
    
]
