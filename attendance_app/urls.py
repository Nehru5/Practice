from django.urls import path
from . import views

urlpatterns = [
  path('mark/<int:student_id>/<uuid:batch_uuid>/<int:trainer_id>/', views.mark_attendance, name='mark_attendance'),


]

