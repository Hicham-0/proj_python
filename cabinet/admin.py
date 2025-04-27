from django.contrib import admin

# Register your models here.
from .models import Medecin, Patient, RendezVous

# Enregistrement des modèles dans l'admin
admin.site.register(Medecin)
admin.site.register(Patient)
admin.site.register(RendezVous)
