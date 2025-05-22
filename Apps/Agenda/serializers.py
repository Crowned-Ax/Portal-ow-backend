from rest_framework import serializers
from .models import Schedule
from ..Usuario.models import User

class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    
    class Meta:
        model = Schedule
        fields = ['id', 'time', 'date', 'priority', 'title', 'subtext', 'completed', 'created_by', 'assigned_to']
        read_only_fields = ['created_by']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.created_by:
            user = User.objects.filter(email=instance.created_by).first()
            data['created_by_name'] = user.get_full_name()
        return data