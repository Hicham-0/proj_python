from django.db import models

# Create your models here.

class Medecin(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    specialite = models.CharField(max_length=50)
    numero_telephone = models.CharField(max_length=15)
    ville = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite} ({self.ville})"

class Patient(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    numero_telephone = models.CharField(max_length=15)
    date_naissance = models.DateField()
    mot_de_passe = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    


class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date = models.DateTimeField()
    motif = models.TextField()
    
    def __str__(self):
        return f"RDV: {self.patient} avec {self.medecin} le {self.date}"

class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dossier médical de {self.patient}"

class Observation(models.Model):
    dossier_medical = models.ForeignKey(DossierMedical, on_delete=models.CASCADE, related_name='observations')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()
    
    def __str__(self):
        return f"Observation du {self.date} par Dr. {self.medecin.nom}"

class Ordonnance(models.Model):
    dossier_medical = models.ForeignKey(DossierMedical, on_delete=models.CASCADE, related_name='ordonnances')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()  # Description des médicaments et posologies
    
    def __str__(self):
        return f"Ordonnance du {self.date} par Dr. {self.medecin.nom}"

class Facture(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('PAYEE', 'Payée'),
    ]
    numero_facture = models.CharField(max_length=20, unique=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_emission = models.DateField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    rendez_vous = models.OneToOneField('RendezVous', on_delete=models.CASCADE, related_name='facture', null=True, blank=True)

    def __str__(self):
        return f"Facture {self.numero_facture}"