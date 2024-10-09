from rest_framework import generics
from .models import Services
from django.shortcuts import get_object_or_404
from .serializers import ServicesSerializer
from ..Clientes.models import Client

# Vista para listar y crear Servicios
class ServicesListCreateView(generics.ListCreateAPIView):
    serializer_class = ServicesSerializer
    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Services.objects.filter(client__id=client_id)

    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        client = get_object_or_404(Client, id=client_id)
        serializer.save(client=client)

# Vista para obtener, actualizar y eliminar un servicio específico
class ServicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Services.objects.filter(client__id=client_id)

