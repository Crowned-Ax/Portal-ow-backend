from django.urls import path, include

urlpatterns = [
    path('Users/', include('Apps.Usuario.urls')),
    path('Clients/', include('Apps.Clientes.urls')),
]
