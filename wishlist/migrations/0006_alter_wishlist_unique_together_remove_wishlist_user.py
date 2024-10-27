# Generated by Django 5.1.1 on 2024-10-26 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('wishlist', '0005_alter_wishlist_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('section', 'menu')},
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
    ]
