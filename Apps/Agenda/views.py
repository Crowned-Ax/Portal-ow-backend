from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Schedule
from ..Usuario.models import User
from .serializers import ScheduleSerializer
from django.core.exceptions import ValidationError
from django.db.models import Q
from ..Notificaciones.models import Notification
from django.utils import timezone

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(
            Q(created_by=self.request.user) | Q(assigned_to=self.request.user)
        )

    def perform_create(self, serializer):
        assigned_email = serializer.initial_data.get('assigned_to')
        if assigned_email and assigned_email != "":
            assigned_user = User.objects.filter(email=assigned_email).first()
            if not assigned_user:
                raise ValidationError("El usuario asignado no es válido.")
            creador = User.objects.filter(email=self.request.user).first()
            Notification.objects.create(
                message=f"{creador.get_full_name()} te asigno una tarea",
                date=timezone.now().date(),
                type="info",
                user=assigned_user
            )
        else:
            assigned_user = self.request.user

        serializer.save(
            created_by=self.request.user,
            assigned_to=assigned_user
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Solo el creador puede eliminar
        if instance.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Solo el creador puede actualizar
        if instance.created_by != request.user and instance.assigned_to != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

