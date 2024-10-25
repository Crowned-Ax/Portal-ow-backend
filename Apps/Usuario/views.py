from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, LoginSerializer, SimpleUserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        if user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Usted no tiene permisos para editar este perfil.")

        return user

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]  # Solo un administrador puede eliminar usuarios

    def get_object(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise generics.Http404
        # Verifica permisos: solo un staff puede eliminar
        if not self.request.user.is_staff:
            raise PermissionDenied("Usted no tiene permisos para eliminar este perfil.")

        return user

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Solo un administrador puede crear superusuarios

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_superuser(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                **serializer.validated_data
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            user_data = SimpleUserSerializer(user).data
            return Response({'token': token.key, 'user': user_data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # El user validado viene del método validate_login
        token, _ = Token.objects.get_or_create(user=user)
        user_data = SimpleUserSerializer(user).data
        return Response({'token': token.key, 'user': user_data})
    
class ChangePasswordView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        # Verificar que la contraseña actual coincida
        if not check_password(current_password, user.password):
            return Response({"detail": "La contraseña actual no es correcta."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que la nueva contraseña cumpla con los requisitos mínimos
        if not new_password or len(new_password) < 8:
            return Response({"detail": "La nueva contraseña debe tener al menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña del usuario
        user.set_password(new_password)
        user.save()

        return Response({"detail": "La contraseña ha sido cambiada exitosamente."}, status=status.HTTP_200_OK)
