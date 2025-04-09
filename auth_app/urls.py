from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='homepage'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('trainer_login/', views.trainer_login, name='trainer_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('logout/', views.user_logout, name='logout'),
]
