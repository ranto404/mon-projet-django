from ast import Add
from .models import Product, Category, Vendor, CardOrder, CardOrderItems, ProductImages, ProductReview, Wishlist
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    
    min_max_price = Product.objects.aaggregate(Min("price"), Max("price"))

    return {
        'categories' : categories,
        'min_max_price' : min_max_price,
    }