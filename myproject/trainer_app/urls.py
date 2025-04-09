from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.trainer_signup, name='trainer_signup'),
    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('logout/', views.trainer_logout, name='trainer_logout'),
    path('scan/', views.trainer_qr_scanner, name='trainer_qr_scanner'),
]
