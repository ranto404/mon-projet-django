from django.urls import path

from .views import *

urlpatterns = [
    path(r"inscrire/",pageinscription,name="inscrire"),
    path(r"inscription/",insertionMembre,name="saveUser"),

    path(r'connexion/',pageconnexion,name="connexion"),
    path(r'login/',connexion,name="seconnecte"),

    path(r'logout/',deconnexion,name="deconnexion"),
    path(r'membre/',membre,name="membre"),
]