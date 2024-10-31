from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    UserDetailView,
    ProfileView,
    UserListView,
    UserDeleteView,
    CreateUserView,
    SimpleUserListView
)

app_name = 'usuario'

urlpatterns = [
    path("", UserListView.as_view(), name='user-list'), # Traer todos los usuarios
    path("simple/", SimpleUserListView.as_view(), name='simple-user-list'), # Traer todos los usuarios con info minima
    path('<str:email>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('colaborator/', CreateUserView.as_view(), name='create-superuser'),
    path("login/", LoginView.as_view(), name="login"), # Loguearse
    path("signup/", RegisterView.as_view(), name="register"), # Registrarse
    path("<str:email>/", UserDetailView.as_view(), name ="user-detail"), #traer/modificar un usuario segun su correo electronico
    path('profile', ProfileView.as_view(), name='profile-edit'), # Cambiar datos del usuario logueado
]