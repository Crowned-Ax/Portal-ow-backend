# Generated by Django 5.1 on 2024-10-20 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Servicios', '0003_remove_services_url_services_cateogry_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='cateogry',
            new_name='category',
        ),
    ]
