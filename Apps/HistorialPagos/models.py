from django.db import models
from django.utils import timezone
from ..Clientes.models import Client
from ..Servicios.models import Services
from ..Usuario.models import User
from django.core.exceptions import ValidationError


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0)

    def clean(self):
        # Validación personalizada para asegurar que solo una sea seleccionada
        if not self.client and not self.collaborator:
            raise ValidationError("Debes seleccionar un cliente o un colaborador.")
        if self.client and self.collaborator:
            raise ValidationError("Solo puedes seleccionar un cliente o un colaborador, no ambos.")
    
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)