import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Apphome.models import CardOrder, Product, CardOrderItems
from .models import Order
from django.views.decorators.csrf import csrf_exempt
import stripe
from dotenv import load_dotenv


load_dotenv()


stripe.api_key = os.environ.get("SECRET_KEY")


@csrf_exempt
def effectuer_paiement(request):
    if request.method == 'POST':
        total_prix = request.POST.get("prixtotal")
        token = request.POST.get("stripeToken")
        print([token,total_prix])
        try:
            # Créer une charge avec Stripe en utilisant le token
            charge = stripe.Charge.create(
                amount=int(total_prix) * 100,
                currency="usd",
                source=token,
                description="Test payment avec django"
            )
            
            
            
            # Si la charge est réussie, afficher un message de succès
            return render(request, "procedureStripe.html", {"message": "Paiement réussi !"})
        except stripe.error.StripeError as e:
            error = "Une erreur s'est produite lors du traitement de votre paiement. Veuillez réessayer plus tard."
            return render(request, "procedureStripe.html", {"error": error})
    else:
        error = "Une erreur s'est produite lors du traitement de votre paiement. Veuillez réessayer plus tard."
        return render(request, "procedureStripe.html", {"error": error})







def success_paypal(request):
    return render(request, "success-payement.html")


def panier(request, pid):
    prod = Product.objects.get(pk=pid)

    if "cart" not in request.session:
        request.session["cart"] = []

    cart = request.session["cart"]
    unique_key = prod.pid

    # Récupération du quantité à partir de CardOrderItems
    try:
        card_order_item = CardOrderItems.objects.get(item=prod)
        quantity = card_order_item.quantity
    except CardOrderItems.DoesNotExist:
        quantity = 0

    obj = {
        "id_prod": unique_key,
        "titre": prod.titre,
        "price": float(prod.price),
        "image": prod.image.url,
        "quantity": quantity,  # quantité récupérée depuis CardOrderItems
    }
    
    product_in_cart = False
    for item in cart:
        if item["id_prod"] == unique_key:
            product_in_cart = True
            break

    if not product_in_cart:
        cart.append(obj)
        request.session.modified = True

    return render(request, "panier.html", {"id": id, "prod_price": float(prod.price)})


def supprimer_panier(request, produit_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        for index, prod in enumerate(cart):
            if prod['id_prod'] == produit_id:
                del cart[index]
                break
        request.session['cart'] = cart
    return render(request, "panier.html", {"id":id})



def procedure_Stripe(request):
    return render(request,"procedureStripe.html")