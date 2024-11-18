from rest_framework import viewsets
from .models import Services
from .serializers import ServicesSerializer
from rest_framework.response import Response

class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class ServicesFiltered(viewsets.ViewSet):
        
    def list(self, request, client_id=None):
        servword = Services.objects.all().exclude(category = "Servicios")
        servservice = Services.objects.filter(category = "Servicios")

        serializer_serv_service = ServicesSerializer(servservice, many=True)
        serializer_serv_word = ServicesSerializer(servword, many=True)

        # Retornar las listas separadas en la respuesta
        return Response({
            'servService':serializer_serv_service.data,
            'servWord': serializer_serv_word.data,
        })
