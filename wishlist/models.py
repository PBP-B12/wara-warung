from django.db import models
from django.contrib.auth.models import User
from menu.models import Menu

class Section(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who owns the section
    name = models.CharField(max_length=255)  # Section name, like "Breakfast", "Lunch"
    
    def __str__(self):
        return self.name
        
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'menu')  # Prevent duplicates per user-menu pair
