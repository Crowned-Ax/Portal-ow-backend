# Generated by Django 5.1 on 2024-10-23 23:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0011_alter_clientservice_expirationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientservice',
            name='expirationDate',
            field=models.DateField(default=datetime.datetime(2024, 11, 22, 23, 29, 36, 165585, tzinfo=datetime.timezone.utc)),
        ),
    ]
