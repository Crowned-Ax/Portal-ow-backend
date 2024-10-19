from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Client, Services, ClientService
from .serializers import ClientSerializer, ServicesSerializer, ClientServiceSerializer

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class ClientServiceViewSet(viewsets.ViewSet):
    def create(self, request, client_id=None):
        serializer = ClientServiceSerializer(data=request.data)
        if serializer.is_valid():
            # Aseguramos que el cliente exista
            try:
                serializer.validated_data['client'] = Client.objects.get(id=client_id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Client.DoesNotExist:
                return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, client_id=None, pk=None):
        try:
            client_service = ClientService.objects.get(id=pk, client_id=client_id)
            client_service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)