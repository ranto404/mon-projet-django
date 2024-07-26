from django.db import models
from shortuuid.django_fields import ShortUUIDField
from AppInscription.models import Membres
from django.utils.html import mark_safe

# Create your models here.


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4,"⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)




class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, length=10, prefix="cat")
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100, default="Categorie")
    image = models.ImageField(upload_to="static/img/category", default="category.jpg")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


    class Meta :
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self) :
        return self.title
    



class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, max_length=20, length=10, prefix='cat', alphabet="abcdef12345")

    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to="static/img/user_directory_path", default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="I am amazing vendor")

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/img/category")
    description = models.TextField(null=True, blank=True)
    adresse = models.TextField(max_length=100, default="123 Main Tree")
    contacte = models.TextField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.TextField(max_length=100, default="100")
    shipping_on_time = models.TextField(max_length=100, default="100")
    authentic_rating = models.TextField(max_length=100, default="100")
    days_return = models.TextField(max_length=100, default="100")
    warranty_period = models.TextField(max_length=100, default="100")

    user = models.ForeignKey(Membres, on_delete=models.SET_NULL, null=True)

    class Meta :
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self) :
        return self.title




class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=20, length=10, prefix='cat', alphabet="abcdef12345")
    titre = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    image = models.ImageField(upload_to="static/img/prods")
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="0.00")
    old_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="0.00")
    
    product_status = models.CharField(max_length=255, choices=STATUS,  default="in_review")


    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=200, prefix="sku", alphabet="1234567890")

    date= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(null=True, blank=True)

    class Meta :
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self) :
        return self.titre
    
    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    



class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    
    class Meta :
        verbose_name_plural = "Product Images"


class Cart(models.Model):
    products = models.ManyToManyField(Product)

class CardOrder(models.Model):

        user= models.ForeignKey(Membres, on_delete=models.CASCADE)
        price= models.DecimalField(max_digits=999999999999, decimal_places=2, default="00")
        paid_status =models.BooleanField(default=False)
        order_date = models.DateTimeField(auto_now_add=True)
    
        product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="processig")

        class Meta:
            verbose_name_plural = "Card Order"



class CardOrderItems(models.Model):
        order = models.ForeignKey(CardOrder, on_delete=models.CASCADE)
        invoice_no = models.CharField(max_length=200)
        product_status = models.CharField(max_length=200)
        item = models.CharField(max_length=200)
        image = models.CharField(max_length=200)
        quantity = models.IntegerField(default="0")
        price= models.DecimalField(max_digits=999999999999, decimal_places=2, default="00")
        total = models.DecimalField(max_digits=999999999999, decimal_places=2, default="000")



        class Meta:
            verbose_name_plural = "Card Order Items"


        def order_img(self):
            return mark_safe('<img src="/static/%s" width="50" height="50" />' % (self.image))
        




class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    user = models.ForeignKey(Membres, on_delete=models.CASCADE) 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name_plural = "Product Reviews"
    
    def __str__(self) :
        return self.product.titre
    
    def get_rating(self) :
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(Membres, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)   
    date = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name_plural = "Wishlists"
    
    def __str__(self):
        return f"{self.user.Pseudo} - {self.product.titre}"