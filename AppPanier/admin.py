from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'adresse', 'amount', 'stripe_charge_id']

admin.site.register(Transaction, TransactionAdmin)
