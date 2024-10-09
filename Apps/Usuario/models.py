from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

IDENTIFICACION_OPCIONES = [
    ('CC', 'Cédula de ciudadanía'),
    ('TI', 'tarjeta de identidad'),
    ('P', 'Pasaporte'),
]

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(primary_key=True)
    # Informacion general
    name = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=15, blank=True)
    eEmail_personal = models.EmailField(max_length=40, blank=True)
    eEmail_laboral = models.EmailField(max_length=40, blank=True)
    birthday = models.DateField(null=True)
    id_type = models.CharField(
        choices=IDENTIFICACION_OPCIONES, 
        default='CC',
        max_length=3,
        verbose_name='Tipo de documento'
    )
    country = models.CharField(max_length=47, blank=True)
    state = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=50, blank=True)
    # campos de Cv
    language = models.CharField(max_length=40, blank=True)
    formation = models.CharField(max_length=50, blank=True)
    knowledge = models.CharField(max_length=50, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    # campos de admin
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def get_full_name(self):
        return self.name +" "+ self.lastname
    
class SocialNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=40, blank=True)
