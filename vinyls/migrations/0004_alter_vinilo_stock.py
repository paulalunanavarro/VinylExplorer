# Generated by Django 5.1.4 on 2024-12-29 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinyls', '0003_vinilo_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinilo',
            name='stock',
            field=models.BooleanField(),
        ),
    ]
