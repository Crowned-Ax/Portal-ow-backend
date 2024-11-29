from rest_framework import serializers
from .models import Client, Contact, ClientService

class ContactSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)
    class Meta:
        model = Contact
        fields = ['id', 'cliente', 'name', 'lastname', 'phone', 'email', 'birthday']
        extra_kwargs = {'cliente': {'write_only': True}}

class SimpleClientSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ['id','fullname']
    
    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"

class ClientSerializer(serializers.ModelSerializer):
    # Incluir contactos como un nested serializer
    contactos = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = "__all__"

    def get_contactos(self, obj):
        contacts = obj.Contactos.all()
        return ContactSerializer(contacts, many=True).data

    def create(self, validated_data):
        contactos_data = validated_data.pop('Contactos', [])
        client = Client.objects.create(**validated_data)
        for contact_data in contactos_data:
            Contact.objects.create(cliente=client, **contact_data)
        return client

    def update(self, instance, validated_data):
        contactos_data = validated_data.pop('Contactos', [])
        # Actualizar datos del cliente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar contactos
        contact_ids = [contact['id'] for contact in contactos_data if 'id' in contact]
        # Eliminar contactos no incluidos en la actualización
        instance.Contactos.exclude(id__in=contact_ids).delete()
        for contact_data in contactos_data:
            if 'id' in contact_data:
                contact = Contact.objects.get(id=contact_data['id'], cliente=instance)
                for attr, value in contact_data.items():
                    setattr(contact, attr, value)
                contact.save()
            else:
                Contact.objects.create(cliente=instance, **contact_data)

        return instance

class ClientServiceSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    expirationDate = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)
    name = serializers.CharField(source='service.__str__', read_only=True)

    class Meta:
        model = ClientService
        fields = ['id','client', 'service', 'price', 'startDate', 'expirationDate', 'name', 'is_recurrent', 'recurrence' ,'is_payed']
