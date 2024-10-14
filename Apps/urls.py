from django.urls import path, include

urlpatterns = [
    path('Users/', include('Apps.Usuario.urls')),
    path('Agenda/', include('Apps.Agenda.urls')),
    path('Clients/', include('Apps.Clientes.urls')),
]
