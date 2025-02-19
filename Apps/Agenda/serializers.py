from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    
    class Meta:
        model = Schedule
        fields = ['id', 'time', 'date', 'priority', 'title', 'subtext', 'completed', 'user']
        read_only_fields = ['user']
