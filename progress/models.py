# progress/models.py

from django.db import models
from accounts.models import User
from content.models import Lesson, Exercise

class StudentProgress(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Non commencé'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    completion_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    completion_date = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    time_spent = models.IntegerField(default=0, help_text="Temps passé en secondes")
    
    class Meta:
        unique_together = ('student', 'lesson')
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.lesson.title} - {self.get_completion_status_display()}"

class ExerciseResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_results')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='student_results')
    score = models.IntegerField()
    max_score = models.IntegerField()
    completion_time = models.IntegerField(help_text="Temps de réalisation en secondes")
    attempt_number = models.IntegerField(default=1)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'exercise', 'attempt_number')
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exercise.title} - Tentative {self.attempt_number}"
    
    @property
    def score_percentage(self):
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0

class StudentAnswer(models.Model):
    result = models.ForeignKey(ExerciseResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('content.Question', on_delete=models.CASCADE, related_name='student_answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Réponse de {self.result.student.get_full_name()} à {self.question.question_text[:30]}..."