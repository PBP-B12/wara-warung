from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

class MenuRating(models.Model):
    menu = models.OneToOneField('menu.Menu', on_delete=models.CASCADE) 
    ratings = GenericRelation(Rating, related_query_name='posts')

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('value'))['value__avg'] or 0

    def total_votes(self):
        return self.ratings.count()

class Review(models.Model):
    menu = models.OneToOneField('menu.Menu', on_delete=models.CASCADE) 
    text = models.CharField(max_length=200)