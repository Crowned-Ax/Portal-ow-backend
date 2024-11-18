from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PaymentHistory
from .serializers import HistorySerializer
from ..Clientes.models import Client
from ..Usuario.models import User

class PaymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = HistorySerializer

    @action(detail=False, methods=['get'], url_path='client/(?P<client_id>[^/.]+)')
    def by_client(self, request, client_id=None):
        client = get_object_or_404(Client, id=client_id)
        payments = PaymentHistory.objects.filter(client=client)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='collaborator/(?P<collabo_id>[^/.]+)')
    def by_collaborator(self, request, collabo_id=None):
        collabo = get_object_or_404(User, email=collabo_id)
        payments = PaymentHistory.objects.filter(collaborator=collabo)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


