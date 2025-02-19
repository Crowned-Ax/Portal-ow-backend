from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Schedule
from ..Usuario.models import User
from .serializers import ScheduleSerializer
from django.core.exceptions import ValidationError

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = serializer.initial_data.get('user')
        if not user or user == "":
            user = self.request.user
        else:
            user = User.objects.filter(email=user).first()
            if not user:
                raise ValidationError("El usuario proporcionado no es válido.")

        serializer.save(user=user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

