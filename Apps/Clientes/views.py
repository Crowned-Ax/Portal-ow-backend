from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from .models import Client, ClientService, TributaryAdd
from ..HistorialPagos.models import PaymentHistory
from .serializers import ClientSerializer, ClientServiceSerializer, SimpleClientSerializer, TributarySerializer
from rest_framework.generics import ListAPIView
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from rest_framework.decorators import action
from ..permissions import IsClient
from rest_framework.exceptions import PermissionDenied
from ..Usuario.models import User
from django.shortcuts import get_object_or_404

# Cliente simplificado
class SimpleClientView(ListAPIView):
    queryset = Client.objects.all().order_by('-updated_at')
    serializer_class = SimpleClientSerializer

# Listar y crear clientes
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        # Si el usuario es un cliente, solo puede ver su propio perfil
        if self.request.user.groups.filter(name="Cliente").exists():
            return Client.objects.filter(email=self.request.user.email)
        # Si no es un cliente, devuelve todos los clientes
        return Client.objects.all().order_by('-updated_at')
    def perform_create(self, serializer):
        # Si el usuario es un cliente, entonces denegado
        if self.request.user.groups.filter(name="Cliente").exists():
            raise PermissionDenied("No tienes permisos para crear un cliente")
        else:
            tributarias = self.request.data.get("tributarys", [])
            client = serializer.save()

            # Si hay info tributaria adicional en la lista, crearlos
            for tributary in tributarias:
                TributaryAdd.objects.create(client=client, **tributary)

# Obtener, actualizar y eliminar un cliente específico
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    def get_queryset(self):
        # Si el usuario es un cliente, solo puede ver su propio perfil
        if self.request.user.groups.filter(name="Cliente").exists():
            return Client.objects.filter(email=self.request.user.email)
        # Si no es un cliente, devuelve todos los clientes
        return Client.objects.all()
    
    def perform_update(self, serializer):
        # Si el usuario es un cliente, solo puede actualizar su propio perfil
        if self.request.user.groups.filter(name="Cliente").exists():
            if serializer.instance.email != self.request.user.email:
                raise PermissionDenied("No puedes actualizar otro cliente")
            serializer.save()
        else:
            serializer.save()

    def perform_destroy(self, instance):
        # Si el usuario es un cliente, no puede hacer nada
        if self.request.user.groups.filter(name="Cliente").exists():
            raise PermissionDenied("No tienes permisos para eliminar")
        else:
            instance.delete()
# Crud servicios de un cliente
class ClientServiceViewSet(viewsets.ViewSet):

    @action(detail=False, permission_classes=[IsClient])
    def create(self, request, client_id=None):
        data = request.data
        data["client"] = client_id
        cantidad = int(data.get("Nrecurrency", 1))  # Cantidad de servicios a crear
        recurrence = data.get("recurrence", "Mensual")  # Recurrencia (Mensual o Anual)

        try:
            # Validamos la existencia del cliente
            Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Validamos el serializer una sola vez para la estructura base
        serializer = ClientServiceSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Definimos el delta en función de la recurrencia
        if recurrence == "Mensual":
            delta = relativedelta(months=1)
        elif recurrence == "Anual":
            delta = relativedelta(years=1)
        else:
            return Response({'error': 'Periodo no válida.'}, status=status.HTTP_400_BAD_REQUEST)

        created_services = []  # Lista para almacenar los servicios creados

        # Obtenemos las fechas iniciales del primer servicio
        current_start_date = serializer.validated_data["startDate"]
        current_expiration_date = serializer.validated_data["startDate"] + delta - timedelta(days=1)

        for i in range(cantidad):
            # Actualizamos las fechas dinámicamente
            data["startDate"] = current_start_date
            data["expirationDate"] = current_expiration_date

            # Serializamos y guardamos el nuevo ClientService
            service_serializer = ClientServiceSerializer(data=data)
            if service_serializer.is_valid():
                client_service = service_serializer.save()
                created_services.append(client_service)

                # Creamos el registro de PaymentHistory
                PaymentHistory.objects.create(
                    date=now().date(),
                    service=client_service.service,
                    client=client_service.client,
                    clientService=client_service,
                    currency= client_service.currency,
                    price=client_service.price,
                    is_payed=client_service.is_payed,
                )

                # Actualizamos las fechas para el próximo servicio
                current_start_date += delta
                current_expiration_date += delta
            else:
                return Response(service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Serializamos todos los servicios creados para la respuesta
        serialized_services = ClientServiceSerializer(created_services, many=True)
        return Response(serialized_services.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, permission_classes=[IsClient])
    def destroy(self, request, client_id=None, pk=None):
        try:
            history = PaymentHistory.objects.filter(clientService=pk).first()
            client_service = ClientService.objects.get(id=pk, client_id=client_id)

            if(history and not client_service.is_payed):
                history.delete()

            client_service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request, client_id=None):
        # Filtrar registros donde la categoría del servicio no sea "Ok Web"
        services_not_ok_web = ClientService.objects.filter(
            client_id=client_id
        ).exclude(service__category="Ok Web").order_by('-updated_at')
        
        # Filtrar registros donde la categoría del servicio sea "Ok Web"
        services_ok_web = ClientService.objects.filter(
            client_id=client_id,
            service__category="Ok Web"
        ).order_by('-updated_at')

        # Serializar ambas listas
        serializer_not_ok_web = ClientServiceSerializer(services_not_ok_web, many=True)
        serializer_ok_web = ClientServiceSerializer(services_ok_web, many=True)

        # Retornar las listas separadas en la respuesta
        return Response({
            'wordpress': serializer_not_ok_web.data,
            'servicios': serializer_ok_web.data
        })

    @action(detail=False, permission_classes=[IsClient])  
    def update(self, request, client_id=None, pk=None):
        data = request.data
        try:
            # Obtenemos el `ClientService` que se va a actualizar
            client_service = ClientService.objects.get(id=pk, client_id=client_id)

            # Calculamos el nuevo `expirationDate` basado en el `startDate`
            recurrence = data.get("recurrence", client_service.recurrence)
            start_date = data.get("startDate", client_service.startDate)  # Obtenemos startDate del request o del objeto
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y").date()

            # Definimos el delta en función de la recurrencia
            if recurrence == "Mensual":
                delta = relativedelta(months=1)
            elif recurrence == "Anual":
                delta = relativedelta(years=1)
            else:
                return Response({'error': 'Recurrencia no válida.'}, status=status.HTTP_400_BAD_REQUEST)

            expiration_date = start_date + delta
            data["expirationDate"] = expiration_date

            # Actualizamos el `ClientService` con el serializer
            serializer = ClientServiceSerializer(client_service, data=data, partial=True)
            if serializer.is_valid():
                # Verificar si hay cambios en `is_payed`
                is_payed_original = client_service.is_payed
                is_payed_nuevo = data.get("is_payed", is_payed_original)

                # Guardamos los cambios en el `ClientService`
                updated_client_service = serializer.save()

                # Actualizamos `PaymentHistory` si `is_payed` cambió
                if is_payed_original != is_payed_nuevo:
                    try:
                        payment_history = PaymentHistory.objects.get(clientService=updated_client_service)
                        payment_history.is_payed = is_payed_nuevo
                        payment_history.date = now().date()
                        payment_history.currency = data.get("currency")
                        payment_history.save()
                    except PaymentHistory.DoesNotExist:
                        return Response({'error': 'Historial de pagos no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ClientService.DoesNotExist:
            return Response({'error': 'Servicio de cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)       
# tributarias adicionales
class TributaryViewSet(viewsets.ViewSet):
    def list(self, request, client_id=None):
        tributaries = TributaryAdd.objects.filter(client_id=client_id)
        serializer = TributarySerializer(tributaries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, permission_classes=[IsClient])
    def destroy(self, request, pk=None):
        tributary = get_object_or_404(TributaryAdd, pk=pk)
        tributary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsClient])  
    def update(self, request, client_id=None, pk=None):
        tributary = get_object_or_404(TributaryAdd, pk=pk)
        serializer = TributarySerializer(tributary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)