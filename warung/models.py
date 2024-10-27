from django.db import models

class Warung(models.Model):
    nama=models.CharField(max_length=100)
    alamat=models.CharField(max_length=100)
    telepon=models.IntegerField()

    def __str__(self):
        return self.nama