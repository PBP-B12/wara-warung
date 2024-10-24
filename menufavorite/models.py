from django.db import models
from django.contrib.auth.models import User  # Menggunakan User model bawaan Django
from menu.models import Menu  # Import Menu dari app menu

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Hubungkan dengan User
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Hubungkan dengan Menu yang ada di wishlist
    added_at = models.DateTimeField(auto_now_add=True)  # Menyimpan waktu penambahan ke wishlist

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.menu.menu}"
