# Generated by Django 5.1.4 on 2024-12-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinyls', '0002_remove_vinilo_tracklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='vinilo',
            name='stock',
            field=models.BooleanField(default=True),
        ),
    ]
