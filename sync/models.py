# sync/models.py

from django.db import models
from accounts.models import User

class Download(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('lesson', 'Leçon'),
        ('exercise', 'Exercice'),
        ('exam', 'Examen'),
        ('resource', 'Ressource'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    content_id = models.IntegerField()
    downloaded_at = models.DateTimeField(auto_now_add=True)
    device_info = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_content_type_display()} {self.content_id}"

class SyncLog(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
    )
    
    SYNC_TYPE_CHOICES = (
        ('upload', 'Téléversement'),
        ('download', 'Téléchargement'),
        ('full', 'Complet'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sync_logs')
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)
    data_size = models.IntegerField(null=True, blank=True, help_text="Taille en KB")
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_sync_type_display()} - {self.started_at.strftime('%d/%m/%Y %H:%M')}"