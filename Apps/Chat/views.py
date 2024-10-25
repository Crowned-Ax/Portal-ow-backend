from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Chat, Message
from ..Usuario.models import User
from ..Usuario.serializers import SimpleUserSerializer
from .serializers import MessageSerializer

class ChatView(APIView):

    def post(self, request, *args, **kwargs):
        # Obtener el usuario que hace la solicitud
        sender = request.user
        recipient = request.data.get('recipient')
        text = request.data.get('text')
        # Verificar que los campos estén presentes
        if not recipient or not text:
            return Response({'error': 'Recipient and text are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener al destinatario
        recipient = get_object_or_404(User, email=recipient)

        # Verificar si ya existe un chat entre los dos usuarios
        chat = Chat.objects.filter(
            (models.Q(person1=sender) & models.Q(person2=recipient)) |
            (models.Q(person1=recipient) & models.Q(person2=sender))
        ).first()

        # Si el chat no existe, crearlo
        if not chat:
            chat = Chat.objects.create(person1=sender, person2=recipient)

        # Crear el mensaje en el chat
        message = Message.objects.create(chat=chat, sender=sender, text=text)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
    

class MessageView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener el usuario que hace la solicitud
        sender = request.user
        recipient = kwargs.get('recipient') 

        # Verificar que el destinatario esté presente
        if not recipient:
            return Response({'error': 'Recipient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener al destinatario
        recipient = get_object_or_404(User, email=recipient)

        # Buscar un chat existente entre los dos usuarios
        chat = Chat.objects.filter(
            (models.Q(person1=sender) & models.Q(person2=recipient)) |
            (models.Q(person1=recipient) & models.Q(person2=sender))
        ).first()

        # Si no se encuentra el chat, retornar un error
        if not chat:
            return Response([], status=status.HTTP_200_OK)

        # Obtener los mensajes ordenados de más antiguo a más reciente
        messages = chat.message_set.order_by('date')
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Contacts(APIView):
    def get(self, request, *args, **kwargs):
        print("entre")
        current_user = request.user
        print(current_user)
        # Obtener todos los usuarios excepto el que hace la petición
        users = User.objects.exclude(email=current_user.email)

        user_data = []

        for user in users:
            #buscar si hay chat
            chat = Chat.objects.filter(
            (models.Q(person1=current_user) & models.Q(person2=user)) |
            (models.Q(person1=user) & models.Q(person2=current_user))
            ).first()
            # Buscar el último mensaje entre el usuario actual y el usuario iterado
            last_message_content = None
            last_message_date = None
            if(chat):
                last_message = chat.message_set.order_by('-date').first()
                if last_message:
                    last_message_content = last_message.text
                    last_message_date = last_message.date

            # Serializa el usuario
            user_serializer = SimpleUserSerializer(user)
            user_info = user_serializer.data

            # Agrega la información del último mensaje
            user_info['last_message'] = last_message_content
            user_info['last_message_date'] = last_message_date

            user_data.append(user_info)

        return Response(user_data, status=status.HTTP_200_OK)