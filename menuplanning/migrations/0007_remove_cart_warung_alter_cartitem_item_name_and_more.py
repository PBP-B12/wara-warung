# Generated by Django 5.1.2 on 2024-10-23 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuplanning', '0006_rename_price_cartitem_item_price_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='warung',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='item_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]