from django.db import models
from ..Usuario.models import User

class Schedule(models.Model):
    time = models.TimeField()
    date = models.DateField()
    color = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    subtext = models.TextField(blank=True,null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date', 'time']

