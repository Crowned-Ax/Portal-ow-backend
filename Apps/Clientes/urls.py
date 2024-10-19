from django.urls import path, include
from .views import ClientListCreateView, ClientDetailView, ContactListCreateView, ContactDetailView, ClientServiceViewSet

urlpatterns = [
    path('', ClientListCreateView.as_view(), name='client-list-create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),  # Opcional
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),  # Opcional
    
    path('<int:client_id>/Access/', include('Apps.Accesos.urls')),
    path('<int:client_id>/Complements/', include('Apps.Complementos.urls')),
    # Servicios del cliente
    path('<int:client_id>/clientservices/', ClientServiceViewSet.as_view({'post': 'create'}), name='create-clientservice'),
    path('<int:client_id>/clientservices/<int:pk>/', ClientServiceViewSet.as_view({'delete': 'destroy'}), name='delete-clientservice'),
]
