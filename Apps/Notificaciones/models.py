from django.db import models
from ..Usuario.models import User

NOTIFICACION_TYPES = [
    ('info', 'Informativo'),
    ('event', 'Evento'),
]

class Notification(models.Model):
    message = models.CharField()
    date = models.DateField()
    type = models.CharField(
        choices=NOTIFICACION_TYPES, 
        default='info',
        max_length=5,
        verbose_name='Tipo de notificacion'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
