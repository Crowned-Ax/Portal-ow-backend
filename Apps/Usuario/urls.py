from django.urls import path
from .views import LoginView, RegisterView, UserDetailView, ChangePasswordView, UserListView

app_name = 'usuario'

urlpatterns = [
    path("", UserListView.as_view(), name='user-list'), # Traer todos los usuarios
    path("login/", LoginView.as_view(), name="login"), # Loguearse
    path("signup/", RegisterView.as_view(), name="register"), # Registrarse
    path("user/<str:email>/", UserDetailView.as_view(), name ="profile"), #traer la info de un usuario segun su correo electronico
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), # Cambiar la contraseña del usuario logueado
]