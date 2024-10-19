from rest_framework import serializers
from .models import Services, ClientService

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientService
        fields = ['client', 'service']

