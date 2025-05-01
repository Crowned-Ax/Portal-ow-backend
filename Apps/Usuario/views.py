from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Role, CustomPermission
from ..Notificaciones.models import Notification
from django.utils import timezone
from .serializers import (UserSerializer,
                          LoginSerializer,
                          SimpleUserSerializer,
                          PasswordResetRequestSerializer,
                          PasswordResetSerializer,
                          RoleSerializer,
                          CustomPermissionSerializer,
                          UserRoleSerializer)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        # Excluir al usuario que hace la petición
        return User.objects.exclude(email=self.request.user.email).order_by('-updated_at')

class SimpleUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise generics.Http404
        # Verifica permisos: el usuario autenticado debe ser el mismo usuario o un staff
        """
        if user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Usted no tiene permisos para editar este perfil.")
        """
        return user

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    #permission_classes = [IsAdminUser]  # Solo un administrador puede eliminar usuarios

    def get_object(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise generics.Http404
        # Verifica permisos: solo un staff puede eliminar
        #if not self.request.user.is_staff:
            #raise PermissionDenied("Usted no tiene permisos para eliminar este perfil.")

        return user

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    #permission_classes = [IsAdminUser]  # Solo un administrador puede crear superusuarios

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data.copy()  # Hacer una copia
            
            email = validated_data.pop('email')
            password = validated_data.pop('password') 
            validated_data.pop('is_staff')
            validated_data.pop('is_superuser')
            validated_data.pop('groups')
            validated_data.pop('user_permissions')

            user = User.objects.create_superuser(
                email=email,
                password=password,
                **validated_data
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # El user validado viene del método validate_login
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        user_data = SimpleUserSerializer(user).data
        return Response({
            'refresh': str(refresh),
            'access': access,
            'user': user_data
        }, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        # Verificar que la contraseña actual coincida
        if not check_password(current_password, user.password):
            return Response({"detail": "La contraseña actual no es correcta."}, status=status.HTTP_400_BAD_REQUEST)
        # Verificar que la nueva contraseña cumpla con los requisitos mínimos
        if not new_password or len(new_password) < 8:
            return Response({"detail": "La nueva contraseña debe tener al menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)
        # Cambiar la contraseña del usuario
        user.set_password(new_password)
        user.save()
        Notification.objects.create(
                message=f"Haz cambiado tu contraseña",
                date=timezone.now().date(),
                type="info",
                user=user
            )
        return Response({"detail": "La contraseña ha sido cambiada exitosamente."}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)

            # Generar el token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construir el enlace de restablecimiento
            frontend_url = "https://okweb.one"
            reset_url = f"{frontend_url}/reset-password/{uid}/{token}/"
            from_email = settings.DEFAULT_FROM_EMAIL

            # Enviar el correo
            send_mail(
                'Recuperación de contraseña',
                f"Usa este enlace para restablecer tu contraseña: {reset_url}",
                from_email,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Correo de recuperación enviado."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class CustomPermissionViewSet(viewsets.ModelViewSet):
    queryset = CustomPermission.objects.all()
    serializer_class = CustomPermissionSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    lookup_field = 'email'
    lookup_value_regex = '[^/]+'
