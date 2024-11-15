from django.db import models

SER_CATEGORY = [
    ('Servicios','Servicios'),
    ('Complemento','Complemento'),
    ('Constructor','Constructor'),
    ('Temas','Temas'),
]

class Services(models.Model):
    name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    img = models.CharField(max_length=50,blank=True,null=True)
    category = models.CharField(
        choices=SER_CATEGORY, 
        default='OK',
        max_length=12,
        verbose_name='Categoria del servicio'
    )
    def __str__(self):
        return f"{self.name}"