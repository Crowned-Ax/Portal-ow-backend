from .models import User, SocialNetwork, CustomPermission, Role
from ..Clientes.models import Client
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ['url']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    social_networks = SocialNetworkSerializer(many=True, read_only=True)
    birthday = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False,  allow_null=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        #Falta incluir logica de redes sociales
        user = User.objects.create_user(**validated_data)
        return user

class SimpleUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'fullname', 'rol', 'photo']

    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.rol and instance.rol.is_staff:
            client = Client.objects.filter(email=instance.email).first()
            data['company_name'] = client.company_name if client else 'OkWeb'

        return data
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")
   
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No hay ningún usuario con este correo electrónico.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if 'new_password' not in data:
            raise serializers.ValidationError("Se requiere una nueva contraseña.")
        return data
    
class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ['id', 'code']

class RoleSerializer(serializers.ModelSerializer):
    permissions = CustomPermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomPermission.objects.all(), write_only=True, source='permissions'
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'is_staff', 'permissions', 'permission_ids']

class UserRoleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    rol = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, source='rol')

    class Meta:
        model = User
        fields = ['email', 'rol', 'role_id']