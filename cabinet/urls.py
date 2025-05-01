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


]
