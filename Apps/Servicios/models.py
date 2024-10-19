from django.db import models
from ..Clientes.models import Client

class Services(models.Model):
    name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)
    img = models.ImageField(blank=True)

class ClientService(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)