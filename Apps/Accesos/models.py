from django.db import models
from ..Clientes.models import Client

class Access(models.Model):
    name = models.CharField(max_length=30, blank=True)
    img = models.ImageField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)