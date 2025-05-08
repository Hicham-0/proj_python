from django.shortcuts import render, redirect
from .models import Medecin, Patient,Facture, RendezVous
from django.contrib import messages
from django.contrib.auth.decorators import login_required 



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
    return render(request,'cabinet/reserverrdv.html')

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
    if request.method == 'POST':
       numfacture=request.POST.get('numfact')
       nom=request.POST.get('nom')
       prenom=request.POST.get('prenom')
       montantnv=request.POST.get('montant')
       datepaiement=request.POST.get('date')
       emailpatt=request.session.get('user_email')
       statut="EN_ATTENTE"
       if numfacture and nom and prenom and montantnv and datepaiement and emailpatt :
           try :
               fact=Facture.objects.get(numero_facture=numfacture,statut_paiement=statut,Nompat=nom,prenompat=prenom,emailpat=emailpatt,montant=montantnv)
               fact.statut_paiement="PAYEE"
               fact.date_paiement=datepaiement
               fact.save()
               return render(request,'cabinet/paiementpat.html',{'form':"paiement validé avec succés"})
           except Facture.DoesNotExist:
                return render(request,'cabinet/paiementpat.html',{'form':"informations invalide"})
    return render(request,'cabinet/paiementpat.html')

    

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
         try:
             fact=Facture.objects.get(emailpat=emailp)
             fact.emailpat=nvemail
             fact.save()
             return render(request,'cabinet/updateprflpat.html',{'msg':"Vos informations ont été mises à jour avec succès"})
         except Facture.DoesNotExist:
               return render(request,'cabinet/updateprflpat.html',{'msg':"Vos informations ont été mises à jour avec succès"})
    return  render(request,'cabinet/updateprflpat.html')
        

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
    return render(request, 'cabinet/main_med.html')

def main_pat(request):
    return render(request, 'cabinet/main_pat.html')



