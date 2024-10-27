from django.db import models

class Menu(models.Model):
    warung=models.CharField(max_length=100)
    menu=models.CharField(max_length=100)
    harga=models.IntegerField()
    gambar=models.CharField(max_length=1000)