from django import forms
from .models import Medecin, Patient



class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'specialite', 'numero_telephone', 'ville']
     

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'numero_telephone', 'date_naissance']
