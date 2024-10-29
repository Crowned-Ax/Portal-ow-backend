from django.db import models
from ..Servicios.models import Services
from ..Complementos.models import Complements
from django.utils import timezone
from datetime import timedelta

IDENTIFICACION_OPCIONES = [
    ('CC', 'Cédula de ciudadanía'),
    ('NIT', 'NIT'),
    ('P', 'Pasaporte'),
    ('CE', 'Cédula de extranjería'),
    ('TI', 'Tarjeta de identidad'),
    ('RC', 'Registro civil'),
    ('NIUP', 'NIUP'),
]
REGIMEN_OPCIONES = [
    ('IVA', 'Responsable de IVA'),
    ('No IVA', 'Responsable de NO IVA')
]
CONTRIBUYENTE_OPCIONES = [
    ('Juridico', 'Pesona juridica'),
    ('Natural', 'Pesona natural')
]
TAX_OPCIONES = [
    ('IVA', 'IVA impuesto sobre las ventas'),
    ('INC', 'INC impuesto nacional al consumo'),
    ('IVA-INC', 'IVA - INC'),
    ('N/A', 'No aplica')
]
TAX_ID_OPCIONES = [
    ('01','Gran contribuyente'),
    ('02','Autorretenedor'),
    ('03','Agente de retencion en el impuesto sobre las ventas'),
    ('04','Regimen simple de tributacion'),
    ('05','R-99-PN'),
    ('06','No aplica'),
    ('07','Otros')
]


class Client(models.Model):
    name = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    tributare_type_id = models.CharField(
        choices=IDENTIFICACION_OPCIONES, 
        default='CC',
        max_length=5,
        verbose_name='Tipo de Identificación Tributaria'
    )
    # Informacion basica
    id_number = models.CharField(max_length=15, blank=False)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    position = models.CharField(max_length=30, blank=True)
    # Informacion tributaria
    mark_name = models.CharField(max_length=30, blank=True)
    corporate_name = models.CharField(max_length=30, blank=True) 
    company_name = models.CharField(max_length=30, blank=True)
    taxpayer_type = models.CharField(
        choices=CONTRIBUYENTE_OPCIONES, 
        default='Natural',
        max_length=10,
        verbose_name='Tipo de contribuyente'
    )
    tax_liability = models.CharField(
        choices=TAX_OPCIONES, 
        default='IVA',
        max_length=8,
        verbose_name='Responsabilidad tributaria'
    )
    tax_id_type = models.CharField(
        choices=TAX_ID_OPCIONES, 
        default='01',
        max_length=55,
        verbose_name='Tipo de identificacion tributaria 2'
    )
    regime_type = models.CharField(
        choices=REGIMEN_OPCIONES, 
        default='IVA',
        max_length=7,
        verbose_name='Tipo de regimen'
    )


class TaxPayer(models.Model):
    paymentDate = models.DateField(default=timezone.now)
    amount = models.IntegerField(default=0)
    paymentMethod = models.CharField(max_length=30)

class Contact(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='Contactos')
    name = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=15, blank=True)
    eEmail = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True)


class ClientService(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    startDate = models.DateField(default=timezone.now) 
    expirationDate = models.DateField(default=timezone.now() + timedelta(days=30)) 
    price = models.IntegerField(default=0)

class ClientComplement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    complement = models.ForeignKey(Complements, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('client', 'complement')