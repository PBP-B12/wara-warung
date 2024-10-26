# models.py
from django.db import models
from django.contrib.auth.models import User
from menu.models import Menu

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True, related_name="wishlist_items")  # Link categories to wishlist items

    def __str__(self):
        return f"{self.user.username}'s Wishlist Item: {self.menu.menu}"
