from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from menu.models import Menu


class MenuRating(models.Model):
    header = models.CharField(max_length=100, default="Header")

    def average_rating(self) -> float:
        return UserRateReview.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.header}: {self.average_rating()}"


class UserRateReview(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.menu.name} - Rating: {self.rating}'