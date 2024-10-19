from rest_framework import generics
from .models import Complements
from .serializers import ComplementSerializer

class ComplementListCreateView(generics.ListCreateAPIView):
    queryset = Complements.objects.all()
    serializer_class = ComplementSerializer

class ComplementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complements.objects.all()
    serializer_class = ComplementSerializer
