# licenses/models.py

from django.db import models
from accounts.models import User
import uuid

class License(models.Model):
    STATUS_CHOICES = (
        ('available', 'Disponible'),
        ('activated', 'Activée'),
        ('expired', 'Expirée'),
    )
    
    LICENSE_TYPE_CHOICES = (
        ('student', 'Élève'),
        ('teacher', 'Enseignant'),
        ('parent', 'Parent'),
        ('school', 'École'),
    )
    
    serial_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    activation_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='licenses')
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPE_CHOICES, default='student')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.serial_number} - {self.get_status_display()} - {self.get_license_type_display()}"

class PaymentTransaction(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Carte de crédit'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
    )
    
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    license = models.OneToOneField(License, on_delete=models.CASCADE, related_name='transaction')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.user.get_full_name()} - {self.amount} FCFA"