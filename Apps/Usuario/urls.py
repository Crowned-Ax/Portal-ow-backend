from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    UserDetailView,
    ChangePasswordView,
    UserListView,
    UserDeleteView,
    CreateUserView,
    SimpleUserListView,
    PasswordResetRequestView,
    PasswordResetView
)

app_name = 'usuario'

urlpatterns = [
    path("change-password/", ChangePasswordView.as_view(), name='change-password'),# Cambiar la contraseña del usuario logueado
    path("simple/", SimpleUserListView.as_view(), name='simple-user-list'), # Traer todos los usuarios con info minima
    path('<str:email>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('colaborator/', CreateUserView.as_view(), name='create-superuser'),
    path("login/", LoginView.as_view(), name="login"), # Loguearse
    path("signup/", RegisterView.as_view(), name="register"), # Registrarse
    path("password-reset-request/", PasswordResetRequestView.as_view(), name='password-reset-request'),
    path("reset-password/", PasswordResetView.as_view(), name='password-reset'),
    path("<str:email>/", UserDetailView.as_view(), name ="user-detail"), #traer/modificar un usuario segun su correo electronico
    path("", UserListView.as_view(), name='user-list') # Traer todos los usuarios
]