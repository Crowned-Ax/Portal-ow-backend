from django.urls import path
from .views import ComplementListCreateView, ComplementDetailView

urlpatterns = [
    path('', ComplementListCreateView.as_view(), name='complement-list'),
    path('<int:pk>/', ComplementDetailView.as_view(), name='complement-detail'),
]
