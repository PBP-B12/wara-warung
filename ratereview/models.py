from django.db import models
from django.contrib.auth.models import User
from menu.models import Menu  # Import the Menu model from the menu app

class Review(models.Model):
    menu = models.ForeignKey(Menu, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.menu.menu} by {self.user.username}"
