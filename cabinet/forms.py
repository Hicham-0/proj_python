from django import forms
from .models import Medecin, Patient, RendezVous, DossierMedical, Observation, Ordonnance, Facture


# Définir les choix pour les villes
class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'specialite', 'numero_telephone', 'ville']
        widgets = {
            'nom': forms.TextInput(),
            'prenom': forms.TextInput(),
            'email': forms.EmailInput(),
            'mot_de_passe': forms.PasswordInput(),
            'specialite': forms.Select(choices=[
                ('generaliste', 'Généraliste'),
                ('cardiologue', 'Cardiologue'),
                ('dermatologue', 'Dermatologue'),
                ('pediatre', 'Pédiatre'),
                ('chirurgien', 'Chirurgien'),
            ]),
            'numero_telephone': forms.TextInput(),
            'ville': forms.Select(choices=[
                ('casablanca', 'Casablanca'),
                ('rabat', 'Rabat'),
                ('marrakech', 'Marrakech'),
                ('tangier', 'Tanger'),
                ('fes', 'Fès'),
            ]),
        }



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'numero_telephone', 'date_naissance']
        widgets = {
            'nom': forms.TextInput(),
            'prenom': forms.TextInput(),
            'email': forms.EmailInput(),
            'mot_de_passe': forms.PasswordInput(),
            'numero_telephone': forms.TextInput(),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }



class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['medecin', 'date', 'motif']
        widgets = {
            'medecin': forms.Select(),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        
        return date

class RechercheMedecinForm(forms.Form):
    CRITERE_CHOICES = [
        ('nom', 'Nom'),
        ('specialite', 'Spécialité'),
        ('ville', 'Ville'),
    ]
    
    critere = forms.ChoiceField(choices=CRITERE_CHOICES)
    terme_recherche = forms.CharField(max_length=100)

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4}),
        }

class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4}),
        }

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['montant', 'numero_facture']
        widgets = {
            'montant': forms.NumberInput(),
            'numero_facture': forms.TextInput(),
        }

    def clean_numero_facture(self):
        numero = self.cleaned_data['numero_facture']
        if Facture.objects.filter(numero_facture=numero).exists():
            raise forms.ValidationError("Ce numéro de facture existe déjà")
        return numero

class LoginForm(forms.Form):
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('medecin', 'Médecin')])

