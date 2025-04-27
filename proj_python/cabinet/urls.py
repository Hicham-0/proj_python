from django.urls import path 

from . import views 

urlpatterns = [

 path("creer_compte", views.creer_compte, name="creer_compte"),
 path("", views.landing, name="landing"),

]
