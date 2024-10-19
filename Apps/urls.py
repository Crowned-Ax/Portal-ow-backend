from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Servicios.views import ServicesViewSet

router = DefaultRouter()
router.register(r'services', ServicesViewSet)

urlpatterns = [
    path('users/', include('Apps.Usuario.urls')),
    path('agenda/', include('Apps.Agenda.urls')),
    path('clients/', include('Apps.Clientes.urls')),
    path('', include(router.urls)),
]
