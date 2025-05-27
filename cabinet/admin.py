from django.contrib import admin

# Register your models here.
from .models import Medecin, Patient, RendezVous, Facture, DossierMedical, Ordonnance, Observation, Notification,Admin

# Enregistrement des modèles dans l'admin
admin.site.register(Medecin)
admin.site.register(Patient)
admin.site.register(RendezVous)
admin.site.register(Facture)
admin.site.register(DossierMedical)
admin.site.register(Ordonnance)
admin.site.register(Observation)
admin.site.register(Notification)
admin.site.register(Admin)
