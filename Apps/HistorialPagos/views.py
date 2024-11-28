from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PaymentHistory
from .serializers import HistorySerializer
from ..Clientes.models import Client
from ..Usuario.models import User

class PaymentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = HistorySerializer
    @action(detail=False, methods=['get'], url_path='clients/')
    def by_clients(self, request):
        payments = PaymentHistory.objects.filter(collaborator=None)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='collaborator/')
    def by_collaborators(self, request):
        payments = PaymentHistory.objects.filter(client=None)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


