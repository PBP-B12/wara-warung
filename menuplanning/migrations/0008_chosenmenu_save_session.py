# Generated by Django 5.1.2 on 2024-10-25 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuplanning', '0007_remove_cart_warung_alter_cartitem_item_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chosenmenu',
            name='save_session',
            field=models.IntegerField(default=0),
        ),
    ]
