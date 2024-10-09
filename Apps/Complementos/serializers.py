from rest_framework import serializers
from .models import Complements

class ComplementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complements
        fields = ['id', 'name', 'description', 'url', 'img', 'client']
