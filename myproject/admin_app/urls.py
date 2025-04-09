from django.urls import path
from . import views

urlpatterns = [
    # path('signup/', views.admin_signup, name='admin_signup'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-batch/', views.create_batch, name='create_batch'),
    path('add-users/', views.add_users_to_batch, name='add_users_to_batch'),
    path('register-student/', views.register_student_by_admin, name='register_student_by_admin'),
     path('register-trainer/', views.register_trainer_by_admin, name='register_trainer_by_admin'),
     path('register-tracker/', views.register_tracker_by_admin, name='register_tracker_by_admin'),
]
     

