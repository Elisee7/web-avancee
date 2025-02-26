# notifications/models.py

from django.db import models
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('achievement', 'Réussite'),
        ('reminder', 'Rappel'),
        ('update', 'Mise à jour'),
        ('message', 'Message'),
        ('exam', 'Examen'),
        ('system', 'Système'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, default='message')
    related_object_type = models.CharField(max_length=100, null=True, blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title} - {self.created_at.strftime('%d/%m/%Y')}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    achievement_notifications = models.BooleanField(default=True)
    reminder_notifications = models.BooleanField(default=True)
    update_notifications = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    exam_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Préférences de notification pour {self.user.get_full_name()}"

class DeviceToken(models.Model):
    DEVICE_TYPE_CHOICES = (
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'token')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_device_type_display()}"