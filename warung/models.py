from django.db import models

# Create your models here.
class Warung(models.Model):
    nama=models.CharField(max_length=100)
    alamat=models.CharField(max_length=100)
    telepon=models.IntegerField()