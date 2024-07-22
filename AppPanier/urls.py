from django.urls import path

from .views import *

urlpatterns = [
    # path("panier/<pid>",panier,name="panier"),
    path(f"effectuer_paiement/",effectuer_paiement,name="effectuer_paiement"),
    path('success_paypal/', success_paypal, name='success_paypal'),
    path("suppre/<produit_id>",supprimer_panier,name="suppre"),
    path(f"stripe/",procedure_Stripe,name="stripe"),
    # path(f"success/",success_paypal,name=""),
]