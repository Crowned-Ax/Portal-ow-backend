from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Complements
from .serializers import ComplementsSerializer
from ..Clientes.models import Client

# Vista para listar y crear complementos de un cliente específico
class ComplementsListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplementsSerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Complements.objects.filter(client__id=client_id)

    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        client = get_object_or_404(Client, id=client_id)
        serializer.save(client=client)

# Vista para obtener, actualizar y eliminar un complemento específico de un cliente
class ComplementsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complements.objects.all()
    serializer_class = ComplementsSerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Complements.objects.filter(client__id=client_id)
