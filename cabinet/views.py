from django.shortcuts import render, redirect
from .models import Medecin, Patient,Facture, RendezVous
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from datetime import datetime, time
from django.http import JsonResponse
import random



def creer_compte(request):
   if request.method =='POST':

    nompat=request.POST.get('nom')
    prenompat=request.POST.get('prenom')
    emailpat=request.POST.get('email')
    mtdppat=request.POST.get('mdp')
    datenaissancepat=request.POST.get('datenaiss')
    numtelpat=request.POST.get('numtel')
    if nompat and prenompat and emailpat and mtdppat and datenaissancepat and numtelpat :
        data=Patient(nom=nompat,prenom=prenompat,email=emailpat,numero_telephone= numtelpat,date_naissance=datenaissancepat,mot_de_passe=mtdppat)
        data.save()
        return render(request, 'cabinet/signup.html', {'form':"votre compte est crée avec succés"})
    else :
        return render(request, 'cabinet/signup.html')

   return render(request, 'cabinet/signup.html')

   
    




def landing(request):
    return render(request, 'cabinet/landing.html')


def services(request):
    return render(request, 'cabinet/services.html')

def reserverrdv(request):
    from .models import Medecin, Patient, RendezVous, Facture
    medecins = Medecin.objects.all()
    horaires_fixes = [time(h, 0) for h in range(8, 17)]  # 8h à 16h
    today = datetime.now().date().isoformat()

    if request.method == 'POST':
        medecin_id = request.POST.get('medecin')
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure')
        motif = request.POST.get('motif')
        if medecin_id and date_str and heure_str and motif:
            medecin = Medecin.objects.get(id=medecin_id)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            heure_obj = datetime.strptime(heure_str, '%H:%M').time()
            datetime_rdv = datetime.combine(date_obj, heure_obj)
            email_patient = request.session.get('user_email')
            patient = Patient.objects.get(email=email_patient)
            if RendezVous.objects.filter(medecin=medecin, date=datetime_rdv).exists():
                messages.error(request, "Ce créneau est déjà réservé.")
            else:
                rdv = RendezVous.objects.create(
                    patient=patient,
                    medecin=medecin,
                    date=datetime_rdv,
                    motif=motif
                )
                numero_facture = f"FCT-{random.randint(10,999)}"
                Facture.objects.create(
                    numero_facture=numero_facture,
                    montant=200,
                    date_emission=datetime.now().date(),
                    statut_paiement='EN_ATTENTE',
                    rendez_vous=rdv
                )
                messages.success(request, "Votre rendez-vous a été réservé avec succès.")
                return redirect('voirhistopat')
    return render(request, 'cabinet/reserverrdv.html', {'medecins': medecins, 'today': today})

def consulterhistoriquepat(request):
    emailp = request.session.get('user_email')
    if not emailp:
        return redirect('login')
    try:
        patient = Patient.objects.get(email=emailp)
        rdvs = RendezVous.objects.filter(patient=patient).order_by('-date')
    except Patient.DoesNotExist:
        rdvs = []
    return render(request, 'cabinet/voirhistopat.html', {'rdvs': rdvs})

def effecpaiementpat(request):
    emailpatt = request.session.get('user_email')
    if not emailpatt:
        return redirect('login')
    from .models import Facture, Patient
    patient = Patient.objects.get(email=emailpatt)
    if request.method == 'POST':
        facture_id = request.POST.get('facture_id')
        try:
            facture = Facture.objects.get(id=facture_id, rendez_vous__patient=patient, statut_paiement='EN_ATTENTE')
            facture.statut_paiement = 'PAYEE'
            facture.date_paiement = datetime.now().date()
            facture.save()
            msg = "Facture payée avec succès."
        except Facture.DoesNotExist:
            msg = "Facture introuvable ou déjà payée."
    else:
        msg = None
    factures = Facture.objects.filter(rendez_vous__patient=patient, statut_paiement='EN_ATTENTE')
    return render(request, 'cabinet/paiementpat.html', {'factures': factures, 'msg': msg})

    

def consultprofilpat(request):
        emailp=request.session.get('user_email')
        mdpp=request.session.get('user_mdp')
        infos=Patient.objects.get(email=emailp,mot_de_passe=mdpp)
        return render(request,'cabinet/consulterprfl.html',{'user':infos})
    
def updateprflpat(request):
    if request.method == 'POST':
         emailp=request.session.get('user_email')
         mdpp=request.session.get('user_mdp')
         nvemail=request.POST.get('email')
         nvtel=request.POST.get('telephone')
         nvdate=request.POST.get('date_naissance')
         nvmdp=request.POST.get('mdp')
         pat=Patient.objects.get(email=emailp,mot_de_passe=mdpp)
         pat.email=nvemail
         pat.numero_telephone = nvtel
         pat.date_naissance = nvdate
         pat.mot_de_passe=nvmdp
         pat.save() 
         return render(request,'cabinet/updateprflpat.html',{'msg':"Vos informations ont été mises à jour avec succès"})

        

def login(request):
    if request.method == 'POST':
       emaila=request.POST.get('email')
       mdpa=request.POST.get('mdp')
       rolea=request.POST.get('role')
       if emaila and mdpa and rolea and rolea =="patient":
           try:
               user=Patient.objects.get(email=emaila,mot_de_passe=mdpa)
               request.session["user_email"]=user.email
               request.session["user_mdp"]=user.mot_de_passe
               request.session["user_role"]="patient"
               return redirect("main_pat")
           except Patient.DoesNotExist:
               return render(request,'cabinet/login.html',{'form':"impossible de se connecter,informations invalide "})
       elif emaila and mdpa and rolea and rolea =="medecin":
           try:
               user=Medecin.objects.get(email=emaila,mot_de_passe=mdpa)
               request.session["user_email"]=user.email
               request.session["user_mdp"]=user.mot_de_passe
               request.session["user_role"]="médecin"
               return redirect("main_med")
           except Medecin.DoesNotExist:
               return render(request,'cabinet/login.html',{'form':"impossible de se connecter,informations invalide "})
    return render(request,'cabinet/login.html')
               

def logout(request):
    request.session.flush()  # Efface toutes les données de session
    return redirect('landing')

def main_med(request):
    email=request.session.get('user_email')
    med=Medecin.objects.get(email=email)
    contexte=med
    return render(request, 'cabinet/main_med.html',{'form':contexte})

def main_pat(request):
    return render(request, 'cabinet/main_pat.html')

def annuler_rdv(request, rdv_id):
    emailp = request.session.get('user_email')
    if not emailp:
        return redirect('login')
    try:
        patient = Patient.objects.get(email=emailp)
        rdv = RendezVous.objects.get(id=rdv_id, patient=patient)
        rdv.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
    except (Patient.DoesNotExist, RendezVous.DoesNotExist):
        messages.error(request, "Impossible d'annuler ce rendez-vous.")
    return redirect('voirhistopat')

def modifier_rdv(request, rdv_id):
    from .models import Medecin, RendezVous, Patient
    from datetime import datetime, time
    emailp = request.session.get('user_email')
    if not emailp:
        return redirect('login')
    try:
        patient = Patient.objects.get(email=emailp)
        rdv = RendezVous.objects.get(id=rdv_id, patient=patient)
    except (Patient.DoesNotExist, RendezVous.DoesNotExist):
        messages.error(request, "Impossible de modifier ce rendez-vous.")
        return redirect('voirhistopat')

    medecins = Medecin.objects.all()
    today = datetime.now().date().isoformat()

    if request.method == 'POST':
        medecin_id = request.POST.get('medecin')
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure')
        motif = request.POST.get('motif')
        if medecin_id and date_str and heure_str and motif:
            medecin = Medecin.objects.get(id=medecin_id)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            heure_obj = datetime.strptime(heure_str, '%H:%M').time()
            datetime_rdv = datetime.combine(date_obj, heure_obj)
            # Vérifier que le créneau est libre ou que c'est le même RDV
            conflit = RendezVous.objects.filter(medecin=medecin, date=datetime_rdv).exclude(id=rdv.id).exists()
            if conflit:
                messages.error(request, "Ce créneau est déjà réservé.")
            else:
                rdv.medecin = medecin
                rdv.date = datetime_rdv
                rdv.motif = motif
                rdv.save()
                messages.success(request, "Le rendez-vous a été modifié avec succès.")
                return redirect('voirhistopat')

    # Pré-remplissage pour le GET ou en cas d'erreur
    context = {
        'medecins': medecins,
        'rdv': rdv,
        'today': today,
    }
    return render(request, 'cabinet/modifier_rdv.html', context)

from datetime import datetime
from django.contrib import messages # type: ignore 

def creneaux_disponibles(request):
    from .models import Medecin, RendezVous
    from datetime import datetime, time
    medecin_id = request.GET.get('medecin')
    date_str = request.GET.get('date')
    horaires_fixes = [time(h, 0) for h in range(8, 17)]  # 8h à 16h
    if not medecin_id or not date_str:
        return JsonResponse({'creneaux': []})
    try:
        medecin = Medecin.objects.get(id=medecin_id)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        rdvs = RendezVous.objects.filter(medecin=medecin, date__date=date_obj)
        heures_prises = [rdv.date.time() for rdv in rdvs]
        horaires_disponibles = [h.strftime('%H:%M') for h in horaires_fixes if h not in heures_prises]
        return JsonResponse({'creneaux': horaires_disponibles})
    except Exception:
        return JsonResponse({'creneaux': []})

def voirrdvmed(request):
    return render(request,'cabinet/voirrdv_med.html')

def voirprflmed(request):
        emailm=request.session.get('user_email')
        mdpm=request.session.get('user_mdp')
        infos=Medecin.objects.get(email=emailm,mot_de_passe=mdpm)
        return render(request,'cabinet/voirprfl_med.html',{'user':infos})

def genfact(request):
    return render(request,'cabinet/genererfacture_med.html')

def createfolder(request):
    return render(request,'cabinet/creerdossier_med.html')


def consultdossier(request):
    return render(request,'cabinet/voirdossier_med.html')

def ajoutordonnance(request):
    return render(request,'cabinet/ajoutordan_med.html')


def ajoutobservation(request):
    return render(request,'cabinet/ajoutobserv_med.html')

def updateprflmed(request):
         if request.method == 'POST':
             
            emailm=request.session.get('user_email')
            mdpm=request.session.get('user_mdp')
            nvemail=request.POST.get('email')
            nvtel=request.POST.get('numero_telephone')
            nvville=request.POST.get('ville')
            nvmdp=request.POST.get('mdp')
            med=Medecin.objects.get(email=emailm,mot_de_passe=mdpm)
            med.email=nvemail
            med.numero_telephone = nvtel
            med.ville = nvville
            med.mot_de_passe=nvmdp
            med.save()
            return render(request,'cabinet/updateprfl_med.html',{'msg':"Vos informations ont été mises à jour avec succès"})
         return render(request,'cabinet/updateprfl_med.html')

    