from django.db import models

SER_CATEGORY = [
    ('OK Web','OK Web'),
    ('Complemento','Complemento'),
    ('Constructor','Constructor'),
]

class Services(models.Model):
    name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    img = models.ImageField(blank=True)
    category = models.CharField(
        choices=SER_CATEGORY, 
        default='OK',
        max_length=12,
        verbose_name='Categoria del servicio'
    )