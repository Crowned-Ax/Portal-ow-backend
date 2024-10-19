from django.urls import path
from .views import ClientServiceViewSet


urlpatterns = [
    path('client/<int:client_id>/clientservices/', ClientServiceViewSet.as_view({'post': 'create'}), name='create-clientservice'),
    path('client/<int:client_id>/clientservices/<int:pk>/', ClientServiceViewSet.as_view({'delete': 'destroy'}), name='delete-clientservice'),
]
