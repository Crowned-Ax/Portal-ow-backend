from rest_framework import serializers
from .models import Client, ClientService

class SimpleClientSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ['id','fullname']
    
    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"

class ClientSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False,  allow_null=True)
    class Meta:
        model = Client
        fields = "__all__"

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client

    def update(self, instance, validated_data):
        # Actualizar datos del cliente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class ClientServiceSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    expirationDate = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)
    name = serializers.CharField(source='service.__str__', read_only=True)

    class Meta:
        model = ClientService
        fields = ['id','client', 'service', 'currency','price', 'startDate', 'expirationDate', 'name', 'is_recurrent', 'recurrence' ,'is_payed']
