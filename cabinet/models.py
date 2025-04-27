from django.db import models

# Create your models here.

class Medecin(models.Model):
  
    
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    specialite = models.CharField(max_length=50)
    numero_telephone = models.CharField(max_length=15)
    ville = models.CharField(max_length=50)  # Liste déroulante des villes

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite} ({self.ville})"






class Patient(models.Model):
    nom = models.CharField(max_length=50)  # Nom du patient
    prenom = models.CharField(max_length=50)  # Prénom du patient
    email = models.EmailField(unique=True)  # Email du patient
    numero_telephone = models.CharField(max_length=15)  # Numéro de téléphone
    date_naissance = models.DateField(  )  # Date de naissance
    mot_de_passe = models.CharField(max_length=128)  # Mot de passe sécurisé
    dossier_medical = models.TextField(blank=True, null=True)  # Dossier médical (contenu textuel)
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.date_naissance})"


class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date = models.DateTimeField()
    motif = models.TextField()

    def __str__(self):
        return f"RDV: {self.patient} avec {self.medecin} le {self.date}"