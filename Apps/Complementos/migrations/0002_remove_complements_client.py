# Generated by Django 5.1 on 2024-10-20 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Complementos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complements',
            name='client',
        ),
    ]