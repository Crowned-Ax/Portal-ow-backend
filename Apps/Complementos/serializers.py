from rest_framework import serializers
from .models import Complements, ClientComplements

class ComplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complements
        fields = '__all__'
