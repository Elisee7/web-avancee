from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
# accounts/views.py

from django.contrib.auth.decorators import login_required

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
#from .serializers import UserSerializer, UserRegistrationSerializer
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password

def login_view(request):
    error = None
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()  # Utiliser email au lieu de username
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Authentification avec email comme identifiant
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.role == role:
                auth_login(request, user)
                #return redirect('student_dashboard')
                return redirect(f'{role}_dashboard')
            else:
                error = f"Rôle incorrect pour ce compte ({user.get_role_display()})"
        else:
            error = "Email ou mot de passe incorrect"
    
    return render(request, 'login.html', {'error': error})


#

def register(request):
    error = None
    context = {}
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validation renforcée
        if password != confirm_password:
            error = "Les mots de passe ne correspondent pas"
        elif User.objects.filter(email=email).exists():
            error = "Cet email est déjà utilisé"
        elif User.objects.filter(username=username).exists():
            error = "Ce nom d'utilisateur existe déjà"
        elif not role:
            error = "Veuillez sélectionner un rôle"
        else:
            try:
                # Utiliser create_user pour le hachage automatique
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    role=role,
                    first_name=first_name,
                    last_name=last_name
                )
                
                auth_login(request, user)
                #return redirect('student_dashboard')
                #return redirect(reverse('student_dashboard', kwargs={'student_id': student.id}))
                return redirect(f'{role}_dashboard')

                
            except Exception as e:
                error = f"Erreur technique : {str(e)}"

        context['error'] = error
        context['form_data'] = request.POST
        
    return render(request, 'register.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')





















#class UserRegistrationView(generics.CreateAPIView):
#    serializer_class = UserRegistrationSerializer
#    permission_classes = [permissions.AllowAny]

#class UserProfileView(generics.RetrieveUpdateAPIView):
#    serializer_class = UserSerializer
#    permission_classes = [permissions.IsAuthenticated]

#    def get_object(self):
#        return self.request.user

#class CustomTokenObtainPairView(TokenObtainPairView):
#    def post(self, request, *args, **kwargs):
#        response = super().post(request, *args, **kwargs)
#        response.data['role'] = self.user.role  # Ajouter le rôle de l'utilisateur dans la réponse
#        return response

