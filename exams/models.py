# exams/models.py

from django.db import models
from django.utils.text import slugify
from accounts.models import User
from content.models import Exercise

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('practice', 'Exercice d\'entraînement'),
        ('mock', 'Examen blanc'),
        ('past_year', 'Examen session antérieure'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES, default='practice')
    time_limit = models.IntegerField(help_text="Temps limite en minutes", null=True, blank=True)
    passing_score = models.IntegerField(default=50, help_text="Score en pourcentage pour réussir")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    year = models.IntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    exercises = models.ManyToManyField(Exercise, through='ExamExercise')
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.get_exam_type_display()})"
    
    @property
    def total_points(self):
        return sum(ee.weight * ee.exercise.points for ee in self.exam_exercises.all())

class ExamExercise(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exam_links')
    weight = models.FloatField(default=1.0)
    order = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('exam', 'exercise')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam.title} - {self.exercise.title}"

class ExamResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    max_score = models.IntegerField()
    completion_time = models.IntegerField(help_text="Temps de réalisation en minutes")
    passed = models.BooleanField(default=False)
    attempt_number = models.IntegerField(default=1)
    completed_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'exam', 'attempt_number')
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.title} - Tentative {self.attempt_number}"
    
    @property
    def score_percentage(self):
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0