from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet

# Crear un router
router = DefaultRouter()

# Registrar el ViewSet en el router
router.register(r'agenda', ScheduleViewSet)

# Incluir las URLs del router
urlpatterns = [
    path('', include(router.urls)),
]

# las url se autogeneran aqui y son sencillas, basandose en la raiz "Agenda"
# solo es cambiar los distintos tipos de peticion (POST, GET, PUT, etc)
# y en los casos donde se requiere especificar como un PUT o DELETE
# GET /Agenda/{id}/
# es solo poner el id del item especifico