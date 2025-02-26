from django.urls import path
from . import views  # Assure-toi que cet import ne crée pas de boucle

urlpatterns = [
    path('', views.index, name='content_index'),  # Route de test
]
