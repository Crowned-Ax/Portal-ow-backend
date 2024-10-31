from .models import User, SocialNetwork
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ['url']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    social_networks = SocialNetworkSerializer(many=True, read_only=True)
    birthday = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        #Falta incluir logica de redes sociales
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Verificar y actualizar contraseña si está presente
        current_password = validated_data.pop("currentPassword", None)
        new_password = validated_data.pop("newPassword", None)
        if current_password and new_password:
            if not check_password(current_password, instance.password):
                raise serializers.ValidationError({"currentPassword": "La contraseña actual no es correcta."})
            if len(new_password) < 8:
                raise serializers.ValidationError({"newPassword": "La nueva contraseña debe tener al menos 8 caracteres."})
            instance.set_password(new_password)

        # Actualizar los demás campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class SimpleUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'fullname', 'position']

    def get_fullname(self, obj):
        return f"{obj.name} {obj.lastname}"

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