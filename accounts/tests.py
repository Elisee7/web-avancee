# accounts/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User

class UserRegistrationTest(TestCase):
    def test_student_registration(self):
        data = {
            'user': {
                'email': 'eleve@ecep.com',
                'username': 'eleve123',
                'password': 'Password123!',
                'confirm_password': 'Password123!',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'role': 'student'
            },
            'class_level': 'CM2'
        }
        response = self.client.post(reverse('user-register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='eleve@ecep.com').exists())