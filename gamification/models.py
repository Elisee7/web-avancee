# gamification/models.py

from django.db import models
from accounts.models import User

class Badge(models.Model):
    BADGE_TYPE_CHOICES = (
        ('completion', 'Complétion'),
        ('achievement', 'Réalisation'),
        ('skill', 'Compétence'),
        ('participation', 'Participation'),
        ('streak', 'Régularité'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    points_required = models.IntegerField(default=0)
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_badge_type_display()})"

class StudentBadge(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_to')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'badge')
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.badge.name}"

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_cost = models.IntegerField()
    icon = models.ImageField(upload_to='rewards/')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.points_cost} points)"

class PointsTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('earned', 'Points gagnés'),
        ('spent', 'Points dépensés'),
        ('bonus', 'Points bonus'),
        ('adjustment', 'Ajustement'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.points} points ({self.get_transaction_type_display()})"