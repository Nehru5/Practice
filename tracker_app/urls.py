from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.tracker_signup, name='tracker_signup'),
    path('login/', views.tracker_login, name='tracker_login'),
    path('dashboard/', views.tracker_dashboard, name='tracker_dashboard'),

    
    path('export/csv/<str:batch_name>/', views.export_csv, name='export_attendance_csv'),
    path('export/pdf/<str:batch_name>/', views.export_pdf, name='export_attendance_pdf'),
]
