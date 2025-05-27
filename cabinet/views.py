from django.shortcuts import render, redirect, get_object_or_404
from .models import Medecin, Patient,Facture, RendezVous, DossierMedical, Ordonnance, Observation, Notification,Admin
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from datetime import datetime, time
from django.http import JsonResponse
import random
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import pywhatkit 
import os

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
        # Création automatique du dossier médical
        DossierMedical.objects.create(patient=data)
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
                # Création de la notification pour le médecin
                message = f"Le patient {patient.nom} {patient.prenom} a réservé un rendez-vous."
                Notification.objects.create(medecin=medecin, message=message)
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
       if emaila and mdpa and rolea =="patient":
           try:
               user=Patient.objects.get(email=emaila,mot_de_passe=mdpa)
               request.session["user_email"]=user.email
               request.session["user_mdp"]=user.mot_de_passe
               request.session["user_role"]="patient"
               return redirect("main_pat")
           except Patient.DoesNotExist:
               return render(request,'cabinet/login.html',{'form':"impossible de se connecter,informations invalide "})
       elif emaila and mdpa and rolea =="medecin":
           try:
               user=Medecin.objects.get(email=emaila,mot_de_passe=mdpa)
               request.session["user_email"]=user.email
               request.session["user_mdp"]=user.mot_de_passe
               request.session["user_role"]="médecin"
               return redirect("main_med")
           except Medecin.DoesNotExist:
               return render(request,'cabinet/login.html',{'form':"impossible de se connecter,informations invalide "})
       elif  emaila and mdpa and  rolea =="admin":
           try:
               user=Admin.objects.get(email=emaila,mot_de_passe=mdpa)
               request.session["user_email"]=user.email
               request.session["user_mdp"]=user.mot_de_passe
               request.session["user_role"]="admin"
               return redirect("main_admin")
           except Admin.DoesNotExist:
               return render(request,'cabinet/login.html',{'form':"impossible de se connecter,informations invalide "})
    return render(request,'cabinet/login.html')
def main_admin(request):
    return render(request,'cabinet/main_admin.html')           

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
    
def voirprflmed(request):
        emailm=request.session.get('user_email')
        mdpm=request.session.get('user_mdp')
        infos=Medecin.objects.get(email=emailm,mot_de_passe=mdpm)
        return render(request,'cabinet/voirprfl_med.html',{'user':infos})






def mes_patients_med(request):
    """
    Vue pour afficher la liste des patients ayant déjà eu un rendez-vous avec le médecin connecté.
    """
    email_med = request.session.get('user_email')
    if not email_med:
        return redirect('login')
    try:
        medecin = Medecin.objects.get(email=email_med)
        # Récupérer tous les patients ayant eu un rendez-vous avec ce médecin (sans doublons)
        patient_ids = RendezVous.objects.filter(medecin=medecin).values_list('patient', flat=True).distinct()
        patients = Patient.objects.filter(id__in=patient_ids)
        return render(request, 'cabinet/mes_patients_med.html', {'patients': patients})
    except Medecin.DoesNotExist:
        messages.error(request, "Médecin non trouvé.")
        return redirect('login')



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


def mes_rdv_med(request):
    email_med = request.session.get('user_email')
    if not email_med:
        return redirect('login')

    try:
        medecin = Medecin.objects.get(email=email_med)
        rdvs = RendezVous.objects.filter(medecin=medecin).order_by('-date')
        return render(request, 'cabinet/mes_rdv_med.html', {'rdvs': rdvs})
    except Medecin.DoesNotExist:
        messages.error(request, "Médecin non trouvé.")
        return redirect('login')

def dossier_patient_med(request, patient_id):
    """
    Vue pour afficher le dossier médical d'un patient (infos, ordonnances, observations) et permettre l'ajout.
    """
    email_med = request.session.get('user_email')
    if not email_med:
        return redirect('login')
    medecin = get_object_or_404(Medecin, email=email_med)
    patient = get_object_or_404(Patient, id=patient_id)
    dossier = DossierMedical.objects.filter(patient=patient).first()
    ordonnances = Ordonnance.objects.filter(dossier_medical=dossier) if dossier else []
    observations = Observation.objects.filter(dossier_medical=dossier) if dossier else []
    msg = None

    # Ajout d'une ordonnance
    if request.method == 'POST' and 'ajouter_ordonnance' in request.POST:
        contenu = request.POST.get('contenu_ordonnance')
        if contenu and dossier:
            Ordonnance.objects.create(dossier_medical=dossier, medecin=medecin, contenu=contenu)
            msg = "Ordonnance ajoutée avec succès."
            ordonnances = Ordonnance.objects.filter(dossier_medical=dossier)
    # Ajout d'une observation
    if request.method == 'POST' and 'ajouter_observation' in request.POST:
        contenu = request.POST.get('contenu_observation')
        if contenu and dossier:
            Observation.objects.create(dossier_medical=dossier, medecin=medecin, contenu=contenu)
            msg = "Observation ajoutée avec succès."
            observations = Observation.objects.filter(dossier_medical=dossier)

    return render(request, 'cabinet/dossier_patient_med.html', {
        'patient': patient,
        'dossier': dossier,
        'ordonnances': ordonnances,
        'observations': observations,
        'msg': msg,
    })

def ajout_ordonnance_patient(request, patient_id):
    email_med = request.session.get('user_email')
    if not email_med:
        return redirect('login')
    medecin = get_object_or_404(Medecin, email=email_med)
    patient = get_object_or_404(Patient, id=patient_id)
    dossier = DossierMedical.objects.filter(patient=patient).first()
    if request.method == 'POST':
        contenu = request.POST.get('contenu_ordonnance')
        if contenu and dossier:
            Ordonnance.objects.create(dossier_medical=dossier, medecin=medecin, contenu=contenu)
            messages.success(request, "Ordonnance ajoutée avec succès.")
            return redirect(reverse('dossier_patient_med', args=[patient.id]))
    return render(request, 'cabinet/ajout_ordonnance_patient.html', {'patient': patient})

def ajout_observation_patient(request, patient_id):
    email_med = request.session.get('user_email')
    if not email_med:
        return redirect('login')
    medecin = get_object_or_404(Medecin, email=email_med)
    patient = get_object_or_404(Patient, id=patient_id)
    dossier = DossierMedical.objects.filter(patient=patient).first()
    if request.method == 'POST':
        contenu = request.POST.get('contenu_observation')
        if contenu and dossier:
            Observation.objects.create(dossier_medical=dossier, medecin=medecin, contenu=contenu)
            messages.success(request, "Observation ajoutée avec succès.")
            return redirect(reverse('dossier_patient_med', args=[patient.id]))
    return render(request, 'cabinet/ajout_observation_patient.html', {'patient': patient})

@csrf_exempt
@require_GET
def notifications_medecin(request):
    email = request.session.get('user_email')
    role = request.session.get('user_role')
    if not email or role != 'médecin':
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    try:
        medecin = Medecin.objects.get(email=email)
    except Medecin.DoesNotExist:
        return JsonResponse({'error': 'Médecin non trouvé'}, status=404)
    notifications = Notification.objects.filter(medecin=medecin, lu=False).order_by('-date_creation')
    data = [
        {
            'id': n.id,
            'message': n.message,
            'date': n.date_creation.strftime('%d/%m/%Y %H:%M'),
        }
        for n in notifications
        
    ]
    return JsonResponse({'notifications': data})

@csrf_exempt
@require_POST
def marquer_notification_lue(request):
    email = request.session.get('user_email')
    role = request.session.get('user_role')
    notif_id = request.POST.get('id')
    if not email or role != 'médecin' or not notif_id:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    try:
        notif = Notification.objects.get(id=notif_id, medecin__email=email)
        notif.lu = True
        notif.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification non trouvée'}, status=404)
    
def voircomptepat_admin(request):
    tab=Patient.objects.all()
    return render(request,'cabinet/voircomptepat_admin.html',{'pat':tab})

def voircomptemed_admin(request):
    tab=Medecin.objects.all()
    return render(request,'cabinet/voircomptemed_admin.html',{'med':tab})

def voifacture_admin(request):
    tab=Facture.objects.filter(statut_paiement='EN_ATTENTE')
    return render(request,'cabinet/voirfact_admin.html',{'fact':tab})

def appliquer_penalite(request, id):
    fact=Facture.objects.get(id=id)
    text=""
    if request.method == "POST":
       
       frais= request.POST.get('montant')
       fact.montant=fact.montant+Decimal(frais) 
       fact.save()
       rdv=fact.rendez_vous;
       pat=rdv.patient;
       tel=pat.numero_telephone;
       text="pénalité attribuée avec succés"
       tel = tel.replace(" ", "").replace("-", "")
       if tel.startswith("0"):
           tel = tel[1:]
           phone = "+212" + tel
       message= f"Bonjour,\nMediPlace vous informe qu’une pénalité a été appliquée à la facture n°{fact.numero_facture}.Le montant total de cette facture s’élève désormais à {fact.montant} dhs.\nNous vous invitons à régler cette somme dans les plus brefs délais afin d’éviter toute nouvelle majoration.\nMerci pour votre compréhension,\nL’équipe MediPlace."
 
       pywhatkit.sendwhatmsg_instantly(phone,message)
       



    return render(request, 'cabinet/penalite_form.html', {'msg':text,'facture':fact})