from django.db import models

# Create your models here.

class Medecin(models.Model):
    VILLES_MAROC = [
        ('casablanca', 'Casablanca'),
        ('rabat', 'Rabat'),
        ('marrakech', 'Marrakech'),
        ('tangier', 'Tanger'),
        ('fes', 'Fès'),
        ('meknes', 'Meknès'),
        ('agadir', 'Agadir'),
        ('oujda', 'Oujda'),
        ('tetouan', 'Tétouan'),
    ]
    
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    specialite = models.CharField(max_length=50, choices=[
        ('generaliste', 'Généraliste'),
        ('cardiologue', 'Cardiologue'),
        ('dermatologue', 'Dermatologue'),
        ('pediatre', 'Pédiatre'),
        ('chirurgien', 'Chirurgien'),
    ])
    numero_telephone = models.CharField(max_length=15)
    ville = models.CharField(max_length=50, choices=VILLES_MAROC)  # Liste déroulante des villes

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite} ({self.ville})"






class Patient(models.Model):
    nom = models.CharField(max_length=50)  # Nom du patient
    prenom = models.CharField(max_length=50)  # Prénom du patient
    email = models.EmailField(unique=True)  # Email du patient
    numero_telephone = models.CharField(max_length=15)  # Numéro de téléphone
    date_naissance = models.DateField()  # Date de naissance
    mot_de_passe = models.CharField(max_length=128)  # Mot de passe sécurisé
    dossier_medical = models.TextField(blank=True, null=True)  # Dossier médical (contenu textuel)
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.date_naissance})"
