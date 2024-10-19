from rest_framework import serializers
from .models import Client, Contact, ClientService, ClientComplement

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'cliente', 'name', 'lastname', 'tel', 'eEmail', 'birthday']
        extra_kwargs = {'cliente': {'write_only': True}}

class ClientSerializer(serializers.ModelSerializer):
    # Incluir contactos como un nested serializer
    contactos = ContactSerializer(many=True, required=False, source='Contactos')
    
    class Meta:
        model = Client
        fields = [
            'id', 'mark_name', 'tributare_type_id', 'id_number', 'corporate_name', 
            'company_name', 'regime_type', 'taxpayer_type', 'tax_liability', 
            'tax_id_type', 'eEmail', 'tel', 'country', 'department', 
            'city', 'address', 'contactos'
        ]

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
    class Meta:
        model = ClientService
        fields = ['client', 'service']

class ClientComplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientComplement
        fields = ['client', 'complement']