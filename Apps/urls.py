from django.urls import path,  include

urlpatterns = [
    path('users/', include('Apps.Usuario.urls')),
    path('', include('Apps.Agenda.urls')), #agenda
    path('clients/', include('Apps.Clientes.urls')),
    path('', include('Apps.Servicios.urls')), #services
    path('complements/', include('Apps.Complementos.urls')), #complements
]
