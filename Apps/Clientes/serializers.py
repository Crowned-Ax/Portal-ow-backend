from rest_framework import serializers
from .models import Client, ClientService, TributaryAdd
from ..Usuario.models import Role

class SimpleClientSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ['id','fullname', 'email', 'photo']

    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"

class ClientSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False,  allow_null=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)
    class Meta:
        model = Client
        fields = "__all__"

    def to_representation(self, instance):
        """Incluir el role del usuario relacionado al serializar"""
        data = super().to_representation(instance)
        data['rol'] = instance.user.rol.id if instance.user and instance.user.rol else None
        return data
    
    def create(self, validated_data):
        r = Role.objects.filter(name="Cliente").first()
        role = validated_data.pop('rol', None)
        client = Client(**validated_data)
        client._pending_role = role.id if role else r
        client.save()
        return client

    def update(self, instance, validated_data):
        role = validated_data.pop('rol', None)
        validated_data.pop('user', None)
        # Actualizar datos del cliente normalmente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Si se recibió role, actualizar el usuario relacionado

        if role:
            instance.user.rol = role
            instance.user.save()
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