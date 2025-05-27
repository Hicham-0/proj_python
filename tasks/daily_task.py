import os
import sys
import pywhatkit 
# le chemin du projet Django (le dossier contenant manage.py)
sys.path.append("C:/Users/hp/Documents/proj_python")

#  Définir le module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj_python.settings')

#  Initialiser Django
import django
django.setup()

# Importer les modèles Django après l'initialisation
from cabinet.models import RendezVous
from datetime import date, timedelta

aujourdhui = date.today()
rdvs=RendezVous.objects.all()
for rdv in rdvs:
    # Vérifie si le rendez-vous est prévu pour demain
    if rdv.date.date() == aujourdhui + timedelta(days=1):
       pat=rdv.patient;
       tel=pat.numero_telephone;
       tel = tel.replace(" ", "").replace("-", "")
       if tel.startswith("0"):
           tel = tel[1:]
           phone = "+212" + tel
           message= message = f"""
Bonjour,

MediPlace vous rappelle que vous avez un rendez-vous prévu **demain** ({rdv.date.strftime('%d/%m/%Y à %Hh%M')}) avec le Dr {rdv.medecin.nom}.

Merci de bien vouloir vous présenter à l'heure prévue ou de modifier votre réservation si nécessaire.

Cordialement,  
L’équipe MediPlace.
"""
 
           pywhatkit.sendwhatmsg_instantly(phone,message)
       

 

