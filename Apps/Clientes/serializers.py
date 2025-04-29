from rest_framework import serializers
from .models import Client, ClientService, TributaryAdd

class SimpleClientSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ['id','fullname']
    
    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"
    
    def validate_rut(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("El archivo RUT debe ser un PDF.")
        return value

    def validate_c_commerce(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("El archivo Cámara de Comercio debe ser un PDF.")
        return value

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

class TributarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TributaryAdd
        fields = '__all__'

    def validate_rut(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("El archivo RUT debe ser un PDF.")
        return value

    def validate_c_commerce(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("El archivo Cámara de Comercio debe ser un PDF.")
        return value