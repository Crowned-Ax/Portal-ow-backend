from django.urls import path,  include

urlpatterns = [
    path('users/', include('Apps.Usuario.urls')),
    path('agenda/', include('Apps.Agenda.urls')),
    path('clients/', include('Apps.Clientes.urls')),
    path('', include('Apps.Servicios.urls')), #services
    path('complements/', include('Apps.Complementos.urls')), #complements
]
