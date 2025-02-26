# gamification/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from progress.models import ExerciseResult
from .models import Badge, StudentBadge

@receiver(post_save, sender=ExerciseResult)
def check_badge_achievement(sender, instance, created, **kwargs):
    if created and instance.score_percentage >= 90:
        badge, _ = Badge.objects.get_or_create(
            name="Maîtrise Parfaite",
            defaults={
                'description': "Score ≥90% à un exercice",
                'badge_type': 'achievement',
                'points_required': 0
            }
        )
        StudentBadge.objects.get_or_create(student=instance.student, badge=badge)