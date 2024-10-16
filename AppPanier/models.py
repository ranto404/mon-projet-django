from django.db import models

# Create your models here.


# class Order(models.Model):
#     name = models.CharField(max_length=255)
#     adresse = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     charge_id = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.name}"


class Transaction(models.Model):
    customer_name = models.CharField(max_length=255)
    adresse = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.stripe_charge_id} - {self.customer_name}"
