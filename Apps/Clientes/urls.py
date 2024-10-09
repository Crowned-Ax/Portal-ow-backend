from django.urls import path, include
from .views import ClientListCreateView, ClientDetailView, ContactListCreateView, ContactDetailView

urlpatterns = [
    path('', ClientListCreateView.as_view(), name='client-list-create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),  # Opcional
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),  # Opcional
    
    path('<int:client_id>/Access/', include('Apps.Accesos.urls')),
    path('<int:client_id>/Complements/', include('Apps.Complementos.urls')),
    path('<int:client_id>/Services/', include('Apps.Servicios.urls')),
]
