from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from .models import Client, Contact, ClientService
from ..HistorialPagos.models import PaymentHistory
from .serializers import ClientSerializer, ContactSerializer, ClientServiceSerializer, SimpleClientSerializer
from rest_framework.generics import ListAPIView
from django.utils.timezone import now

# Cliente simplificado
class SimpleClientView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = SimpleClientSerializer

# Listar y crear clientes
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Obtener, actualizar y eliminar un cliente específico
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# CRUD para Contact (si necesitas manejo independiente)
class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ClientServiceViewSet(viewsets.ViewSet):
    def create(self, request, client_id=None):
        data = request.data
        data["client"] = client_id
        serializer = ClientServiceSerializer(data=data)
        if serializer.is_valid():
            try:
                client_service = serializer.save()

                PaymentHistory.objects.create(
                    date=now().date(),
                    service=client_service.service,
                    client=client_service.client,  
                    price=client_service.price,  
                    is_payed=client_service.is_payed,  
                )
                client_service_serializer = ClientServiceSerializer(client_service)
                return Response(client_service_serializer.data, status=status.HTTP_201_CREATED)
            except Client.DoesNotExist:
                return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, client_id=None, pk=None):
        try:
            client_service = ClientService.objects.get(id=pk, client_id=client_id)
            client_service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request, client_id=None):
        # Filtrar registros donde la categoría del servicio no sea "Ok Web"
        services_not_ok_web = ClientService.objects.filter(
            client_id=client_id
        ).exclude(service__category="Ok Web")
        
        # Filtrar registros donde la categoría del servicio sea "Ok Web"
        services_ok_web = ClientService.objects.filter(
            client_id=client_id,
            service__category="Ok Web"
        )

        # Serializar ambas listas
        serializer_not_ok_web = ClientServiceSerializer(services_not_ok_web, many=True)
        serializer_ok_web = ClientServiceSerializer(services_ok_web, many=True)

        # Retornar las listas separadas en la respuesta
        return Response({
            'wordpress': serializer_not_ok_web.data,
            'servicios': serializer_ok_web.data
        })

    def update(self, request, client_id=None, pk=None):
        try:
            client_service = ClientService.objects.get(id=pk, client_id=client_id)
            serializer = ClientServiceSerializer(client_service, data=request.data, partial=True)
            if serializer.is_valid():
                 # Verificar si hay cambios en is_payed
                is_payed_original = client_service.is_payed
                is_payed_nuevo = request.data.get("is_payed", is_payed_original)

                # Actualizar ClientService
                serializer.save()
                
                # Solo actualiza PaymentHistory si is_payed cambia
                if is_payed_original != is_payed_nuevo:
                    PaymentHistory.objects.filter(
                        service=client_service.service,
                        client=client_service.client,
                        price=client_service.price
                    ).update(is_payed=is_payed_nuevo, date=now().date(), time=now().time() )
                    
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientService.DoesNotExist:
            return Response({'error': 'Servicio de cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)