# Generated by Django 5.1.1 on 2024-10-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='gambar',
            field=models.CharField(max_length=1000),
        ),
    ]
