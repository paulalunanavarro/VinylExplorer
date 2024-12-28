# Generated by Django 5.1.4 on 2024-12-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vinilo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('precio', models.CharField(max_length=50)),
                ('artista', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('tracklist', models.JSONField()),
                ('imagen', models.URLField()),
            ],
        ),
    ]
