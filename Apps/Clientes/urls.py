from django.urls import path, include
from .views import ClientListCreateView, ClientDetailView, ClientServiceViewSet, SimpleClientView

urlpatterns = [
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    #Accesos
    path('<int:client_id>/Access/', include('Apps.Accesos.urls')),
    # Servicios del cliente
    path('<int:client_id>/clientservices/', 
         ClientServiceViewSet.as_view({'post': 'create', 'get': 'list'}), 
         name='clientservice-list-create'),
    path('<int:client_id>/clientservices/<int:pk>/', 
         ClientServiceViewSet.as_view({'delete': 'destroy', 'put': 'update'}), 
         name='clientservice-detail-update'),
    #Principal
    path('', ClientListCreateView.as_view(), name='client-list-create'),
    path('simple/', SimpleClientView.as_view(), name='simple-client-list')#clientes simplificados
]
