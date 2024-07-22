from django.contrib import admin
from Apphome.models import Product, Category, Vendor, CardOrder, CardOrderItems, ProductImages, ProductReview, Wishlist

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines =  [ProductImagesAdmin]
    list_display = ['titre', 'product_image', 'price', 'featured', 'product_status', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_image', 'name']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_image']


class CardOrderAdmin(admin.ModelAdmin):
    list_display = ['price', 'paid_status', 'order_date', 'product_status']


class CardOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'quantity', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'date']




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CardOrder, CardOrderAdmin)
admin.site.register(CardOrderItems, CardOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)


