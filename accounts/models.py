# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        if not username:
            raise ValueError('Le nom d\'utilisateur est obligatoire')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Élève'),
        ('teacher', 'Enseignant'),
        ('parent', 'Parent'),
        ('admin', 'Administrateur'),
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    serial_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_parent(self):
        return self.role == 'parent'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    class_level = models.CharField(max_length=20, default='CM2')
    birth_date = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.class_level}"

class ParentChild(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parents')
    
    class Meta:
        unique_together = ('parent', 'child')
    
    def __str__(self):
        return f"{self.parent.get_full_name()} - {self.child.get_full_name()}"