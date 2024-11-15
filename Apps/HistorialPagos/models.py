from django.db import models
from django.utils import timezone
from ..Clientes.models import Client
from ..Servicios.models import Services

PAYMENT_TYPE = [
    ('Trans','Transferencia'),
    ('Efect','Efectivo'),

]

class PaymentHistory(models.Model):
    date = models.DateField(default=timezone.now) 
    time = models.TimeField()
    paymentType = models.CharField(
        choices=PAYMENT_TYPE, 
        default='trans',
        max_length=12,
        verbose_name='Tipo de pago'
    )
    bank = models.CharField(max_length=40)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)