# Generated by Django 5.1 on 2024-10-14 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('img', models.ImageField(blank=True, upload_to='')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clientes.client')),
            ],
        ),
    ]
