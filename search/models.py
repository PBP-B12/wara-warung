from django.db import models
from menu.models import Menu

# Create your models here.
class Filter(models.Model):
    harga = models.IntegerField()
    menus = models.ManyToManyField(Menu)

    def __str__(self):
        return f"Filter for price less than {self.harga}"