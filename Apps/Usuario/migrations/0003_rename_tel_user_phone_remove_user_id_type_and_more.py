# Generated by Django 5.1 on 2024-10-22 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0002_rename_eemail_user_eemail_laboral_user_birthday_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='tel',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id_type',
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='documentNumber',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='documentType',
            field=models.CharField(choices=[('CC', 'Cédula de ciudadanía'), ('TI', 'tarjeta de identidad'), ('CE', 'Cédula de extranjería'), ('P', 'Pasaporte')], default='CC', max_length=3, verbose_name='Tipo de documento'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
