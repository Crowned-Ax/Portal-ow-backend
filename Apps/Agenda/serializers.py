from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'time', 'date', 'color', 'title', 'subtext', 'completed', 'user']
        read_only_fields = ['user']
