from django.shortcuts import render, redirect
from .forms import MedecinForm, PatientForm
from django.contrib.auth.decorators import login_required 


def creer_compte(request):
    role = request.POST.get('role') or request.GET.get('role')  # Vérifie d'abord dans POST, puis dans GET

    if request.method == 'POST':
        print("Données POST :", request.POST)
        if role == 'medecin':
            form = MedecinForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
            else:
                print("Erreurs Formulaire Médecin :", form.errors)
        elif role == 'patient':
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('success_page')
            else:
                print("Erreurs Formulaire Patient :", form.errors)
        else:
            form = None
    else:
        if role == 'medecin':
            form = MedecinForm()
        elif role == 'patient':
            form = PatientForm()
        else:
            form = None  # Aucun formulaire sans rôle

    return render(request, 'cabinet/signup.html', {'form': form, 'role': role})




@login_required
def landing(request):
    return render(request, 'cabinet/landing.html')


def services(request):
    return render(request, 'cabinet/services.html')


def propos(request):
    return render(request, 'cabinet/apropos.html')


def login(request):

    return render(request, 'cabinet/login.html')