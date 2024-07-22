from django.contrib import admin
from .models import Order

# Register your models here.



class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'adresse', 'amount', 'charge_id']



admin.site.register(Order, OrderAdmin)


