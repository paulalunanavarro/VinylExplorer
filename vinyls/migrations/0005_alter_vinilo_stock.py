# Generated by Django 5.1.4 on 2024-12-30 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinyls', '0004_alter_vinilo_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinilo',
            name='stock',
            field=models.CharField(max_length=50),
        ),
    ]
