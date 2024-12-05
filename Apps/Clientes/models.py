from django.db import models
from ..Servicios.models import Services
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
    ('Juridico', 'Persona juridica'),
    ('Natural', 'Persona natural')
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

RECURRENCE_OPCIONES = [
    ('Mensual', 'Mensual'),
    ('Anual', 'Anual')
]

class Client(models.Model):
    name = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    documentType = models.CharField(
        choices=IDENTIFICACION_OPCIONES, 
        default='CC',
        max_length=5,
        verbose_name='Tipo de Identificación'
    )
    # Informacion basica
    documentNumber = models.CharField(max_length=15, blank=False)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    position = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to="Profile/Clients",blank=True,null=True)
    # Informacion tributaria
    mark_name = models.CharField(max_length=30, blank=True)
    corporate_name = models.CharField(max_length=30, blank=True) 
    company_name = models.CharField(max_length=30, blank=True)
    tributary_id = models.CharField(max_length=30, blank=True)
    tributary_number = models.CharField(max_length=30, blank=True)
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
    # interno
    updated_at = models.DateTimeField(auto_now=True)

def default_expiration_date():
    return timezone.now() + timedelta(days=30)

class ClientService(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    startDate = models.DateField(default=timezone.now) 
    expirationDate = models.DateField(default=default_expiration_date)
    price = models.IntegerField(default=0)
    is_recurrent = models.BooleanField(default=False)
    recurrence = models.CharField(
        choices=RECURRENCE_OPCIONES, 
        default='Mensual',
        max_length=8,
        verbose_name='Recurrencia'
    )
    is_payed = models.BooleanField(default=False)
    #interno
    updated_at = models.DateTimeField(auto_now=True) 
