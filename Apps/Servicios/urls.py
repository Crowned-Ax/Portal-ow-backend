from django.urls import path
from .views import ServicesListCreateView, ServicesDetailView

urlpatterns = [
    path('', ServicesListCreateView.as_view(), name='services-list-create'),
    path('<int:pk>/', ServicesDetailView.as_view(), name='services-detail'),
]
