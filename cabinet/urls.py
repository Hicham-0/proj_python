from django.urls import path 

from . import views 

urlpatterns = [

 path("creer_compte/", views.creer_compte, name="creer_compte"),
 path("login/", views.login, name="login"),
 path("", views.landing, name="landing"),
 path("services/", views.services, name="services"),
 path("apropos/", views.propos, name="propos"),

]
