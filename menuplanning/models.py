# menuplanning/models.py

from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    budget = models.DecimalField(max_digits=10, decimal_places=2) 


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.item_price


class ChosenMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} for {self.user}"
