from django import forms
from .models import Medecin, Patient


# Définir les choix pour les villes
class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'specialite', 'numero_telephone', 'ville']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            'specialite': forms.Select(choices=[
                ('generaliste', 'Généraliste'),
                ('cardiologue', 'Cardiologue'),
                ('dermatologue', 'Dermatologue'),
                ('pediatre', 'Pédiatre'),
                ('chirurgien', 'Chirurgien'),
            ], attrs={'class': 'form-select'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.Select(choices=[
                ('casablanca', 'Casablanca'),
                ('rabat', 'Rabat'),
                ('marrakech', 'Marrakech'),
                ('tangier', 'Tanger'),
                ('fes', 'Fès'),
            ], attrs={'class': 'form-select'}),
        }



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'numero_telephone', 'date_naissance']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

