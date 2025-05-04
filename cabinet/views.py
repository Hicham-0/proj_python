from django.shortcuts import render, redirect
from .forms import MedecinForm, PatientForm, LoginForm
from .models import Medecin, Patient
from django.contrib import messages
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
                return redirect('login')
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





def landing(request):
    return render(request, 'cabinet/landing.html')


def services(request):
    return render(request, 'cabinet/services.html')

def reserverrdv(request):
    return render(request,'cabinet/reserverrdv.html')

def consulterhistoriquepat(request):
    return render (request,'cabinet/voirhistopat.html')

def effecpaiementpat(request):
    return render(request,'cabinet/paiementpat.html')

def consultprofilpat(request):
    return render(request,'cabinet/consulterprfl.html')



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            role = form.cleaned_data['role']

            if role == 'patient':
                try:
                    patient = Patient.objects.get(email=email, mot_de_passe=mot_de_passe)
                    request.session['user_id'] = patient.id
                    request.session['user_type'] = 'patient'
                    return redirect('main_pat')
                except Patient.DoesNotExist:
                    messages.error(request, "Email ou mot de passe incorrect")
            else:
                try:
                    medecin = Medecin.objects.get(email=email, mot_de_passe=mot_de_passe)
                    request.session['user_id'] = medecin.id
                    request.session['user_type'] = 'medecin'
                    return redirect('main_med')
                except Medecin.DoesNotExist:
                    messages.error(request, "Email ou mot de passe incorrect")
    else:
        form = LoginForm()
    
    return render(request, 'cabinet/login.html', {'form': form})

def logout(request):
    request.session.flush()  # Efface toutes les données de session
    return redirect('landing')

@login_required
def main_pat(request):
    if request.session.get('user_type') != 'patient':
        return redirect('main_med')
    return render(request, 'cabinet/main_pat.html')

@login_required
def main_med(request):
    if request.session.get('user_type') != 'medecin':
        return redirect('main_pat')
    return render(request, 'cabinet/main_med.html')