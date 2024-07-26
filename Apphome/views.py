from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests

from AppInscription.models import Membres

from .form import PriceSearchForm, ProductReviewForm

# Importena ilay table
from .models import Category, Product, Vendor, ProductReview, Cart
from django.views.decorators.http import require_POST
import stripe
from .models import CardOrder
from django.conf import settings
from django.db.models import Min, Max
from django.contrib import messages
from django.db.models import Avg
from django.utils import timezone





stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def home(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('products', 'children', 'children__products')
    products = Product.objects.filter(product_status="published", featured=True)

    # Récupérer les 3 derniers produits ajoutés
    latest_products = Product.objects.order_by('-id')[:3]
    
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))
    form = PriceSearchForm(request.GET or None)


    if form.is_valid():
        max_price = form.cleaned_data.get('max_price')
        if max_price:
            products = products.filter(price__lte=max_price)

    data = {
        'prod': products,
        'categories': categories,
        'latest_products': latest_products,
        'form' : form,
        'min_max_price': min_max_price,

    }

    return render(request, "index.html", data)


def category_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    data = {
        'prod': products,
        'category': category,

    }

    return render(request, "category_list.html", data)


def insertComs(request):
    if request.method == 'POST':
        id_membre = request.session['client']['id']
        id_pro = request.POST.get("id_produit")
        coms = request.POST.get("coms")
        timestamp = timezone.now().strftime('%Y-%m-%d')
        rating = request.POST.get("rating")

        if not id_membre:
            messages.error(request, "Vous devez être connecté pour laisser un commentaire.")
            return redirect('detail', x=id_pro)

        if not coms:
            messages.error(request, "Le commentaire ne peut pas être vide.")
            return redirect('detail', x=id_pro)

        try:
            rating = int(rating)  # Conversion du rating en entier
            if rating < 1 or rating > 5:
                raise ValueError("La note doit être comprise entre 1 et 5.")
        except (ValueError, TypeError):
            messages.error(request, "La note est invalide.")
            return redirect('detail', x=id_pro)

        produit = get_object_or_404(Product, id=id_pro)
        membre = get_object_or_404(Membres, id=id_membre)

        commentaire = ProductReview(
            product=produit,
            user=membre,
            review=coms,
            date=timezone.now().date(),
            rating=rating
        )
        commentaire.save()

        messages.success(request, "Votre commentaire a été envoyé avec succès!")
        return redirect('detail', x=id_pro)

    return redirect('detail', x=id_pro)    



def detail(request,x):

    # x : id anilay produit rehefa azo
    prod = Product.objects.get(pk=x)
    commentaires = ProductReview.objects.filter(product=x).select_related('user')

    avg_rating = commentaires.aggregate(Avg('rating'))['rating__avg']

    # if request.method == 'POST':
    #     form = ProductReviewForm(request.POST)
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.product = prod
    #         review.user = request.user
    #         review.save()
    #         return redirect('detail', x)
    # else:
    #     form = ProductReviewForm()


    data = {
        'produit': prod,
        # 'review': review,
        # 'form': form,
        "coms": commentaires,
        "nbcoms": commentaires.count(),
        "avg_rating": avg_rating

    }
    return render(request,"detail.html", data)

def vendor_list_view(request):
    vendor = Vendor.objects.all()
    data = {
        "vendor" : vendor,
    }
    return render(request,"vendor_list.html", data)


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(titre=query).order_by("-date")

    data = {
        "prod" : products,
        "query" : query,
    }

    return render(request, "search_list.html", data)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    cart.save()
    
    # Mettre à jour le nombre d'articles dans le panier dans la session
    request.session['cart_item_count'] = cart.products.count()
    
    return JsonResponse({'item_count': cart.products.count()})
    
#  -------------------------   #
def checkout(request):
     # Récupérer le panier de la session
    cart = request.session.get('cart', [])
    return render(request, "panier.html", {"cart": cart})


@require_POST
def effectuer_paiement(request):
    nom = request.POST.get('nom')
    adresse = request.POST.get('adresse')
    mois_exp = request.POST.get('card-expiry-month')
    annee_exp = request.POST.get('card-expiry-year')
    nom_carte = request.POST.get('card-name')
    numero_carte = request.POST.get('card-number')
    cvc = request.POST.get('card-cvc')
    prixtotal = request.POST.get('prixtotal')

    try:
        # Créer la charge Stripe
        charge = stripe.Charge.create(
            amount=int(float(prixtotal) * 100),  # Convertir le montant en cents
            currency='eur',
            source=numero_carte,
            description='Paiement pour commande',
            metadata={
                'nom': nom,
                'adresse': adresse,
                'mois_exp': mois_exp,
                'annee_exp': annee_exp,
                'nom_carte': nom_carte,
                'cvc': cvc,
            }
        )

        # Enregistrer la commande dans la base de données
        order = CardOrder.objects.create(
            nom=nom,
            adresse=adresse,
            prix_total=prixtotal,
            # Ajoutez d'autres champs de modèle si nécessaire
        )

        messages.success(request, 'Paiement effectué avec succès!')

        return redirect('page_de_confirmation')  # Rediriger vers une page de confirmation

    except stripe.error.CardError as e:
        # Si la carte est refusée, afficher une erreur
        body = e.json_body
        err = body.get('error', {})
        messages.error(request, f"{err.get('message')} Code d'erreur: {err.get('code')}")
        return redirect('page_d_erreur')  # Rediriger vers une page d'erreur

    except Exception as e:
        # Gérer d'autres erreurs
        messages.error(request, str(e))
        return redirect('page_d_erreur')
    

    