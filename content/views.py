from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate


# Create your views here.
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "L'API content fonctionne correctement"})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):
    #return render(request, 'student_dashboard.html')
    user = request.user  # Récupère l'utilisateur connecté
    if user.is_authenticated:  # Vérifie s'il est connecté
        return render(request, 'student_dashboard.html', {'user': user})
    else:
        return redirect('login')  # Redirige si l'utilisateur n'est pas connecté



def teacher_dashboard(request):
    return JsonResponse({"message": "Tableau de bord de l'enseignant"})

def parent_dashboard(request):
    return JsonResponse({"message": "Tableau de bord du parent"})
