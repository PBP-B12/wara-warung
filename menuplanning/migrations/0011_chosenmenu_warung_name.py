# Generated by Django 5.1.3 on 2024-12-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuplanning', '0010_chosenmenu_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='chosenmenu',
            name='warung_name',
            field=models.CharField(default='Unknown', max_length=255),
        ),
    ]
