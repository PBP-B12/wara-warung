# Generated by Django 5.1.2 on 2024-10-25 15:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_remove_section_created_at_remove_wishlist_added_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
