from django.shortcuts import render, redirect
from .forms import MedecinForm, PatientForm

def creer_compte(request):
    if request.method == 'POST':
        # Récupère le rôle sélectionné
        role = request.POST.get('role')

        # Choix du formulaire basé sur le rôle
        if role == 'medecin':
            form = MedecinForm(request.POST)
        else:
            form = PatientForm(request.POST)

        # Valide et sauvegarde le formulaire si valide
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion
    else:
        # Récupère le rôle via une requête GET ou utilise "patient" par défaut
        role = request.GET.get('role', 'patient')

        # Affiche le bon formulaire sans validation
        form = MedecinForm() if role == 'medecin' else PatientForm()

    return render(request, 'cabinet/signup.html', {'form': form, 'role': role})

def landing(request):
    return render(request, 'cabinet/landing.html')

