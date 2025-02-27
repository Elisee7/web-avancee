from django.urls import path
from . import views  # Assure-toi que cet import ne crée pas de boucle
from .views import student_dashboard, teacher_dashboard, parent_dashboard

urlpatterns = [
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('parent_dashboard/', parent_dashboard, name='parent_dashboard'),
]
