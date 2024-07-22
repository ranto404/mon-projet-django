from django.db import models

# Create your models here.


class Order(models.Model):
    name = models.CharField(max_length=255)
    adresse = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charge_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.name}"