from django.urls import path 

from . import views 

urlpatterns = [

 path("creer_compte/", views.creer_compte, name="creer_compte"),
 path("login/", views.login, name="login"),
 path("logout/", views.logout, name="logout"),
 path("", views.landing, name="landing"),
 path("services/", views.services, name="services"),
 path("main_pat/", views.main_pat, name="main_pat"),
 path("main_med/", views.main_med, name="main_med"),

path('reserverrdv/', views.reserverrdv, name='reserverrdv'),
path("voirhistopat/", views.consulterhistoriquepat, name="voirhistopat"),

path("payerpat/", views.effecpaiementpat, name="payerpat"),
path("consultprflpat/", views.consultprofilpat, name="consultprflpat"),

path("updateprflpat/", views.updateprflpat, name="updateprflpat"),
path("annuler_rdv/<int:rdv_id>/", views.annuler_rdv, name="annuler_rdv"),
path("modifier_rdv/<int:rdv_id>/", views.modifier_rdv, name="modifier_rdv"),
path('creneaux_disponibles/', views.creneaux_disponibles, name='creneaux_disponibles'),


path('mes-rdv-med/', views.mes_rdv_med, name='mes_rdv_med'),
path("voirprflvmed/",views.voirprflmed,name="voirprflmed"),


path("genfact/",views.genfact,name="genfact"),
path("createfolder/",views.createfolder,name="createfolder"),

path("consultdossier/",views.consultdossier,name="consultdossier"),
path("ajoutordonnance/",views.ajoutordonnance,name="ajoutordonnance"),

path("ajoutobservation/",views.ajoutobservation,name="ajoutobservation"),
path("updateprflmed/",views.updateprflmed,name="updateprflmed"),


]
