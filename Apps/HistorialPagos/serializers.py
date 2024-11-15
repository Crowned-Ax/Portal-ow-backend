from rest_framework import serializers
from .models import PaymentHistory

class HistorySerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    class Meta:
        model = PaymentHistory
        fields = '__all__'
