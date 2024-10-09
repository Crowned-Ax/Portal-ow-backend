from django.urls import path
from .views import ComplementsListCreateView, ComplementsDetailView

urlpatterns = [
    path('', ComplementsListCreateView.as_view(), name='complements-list-create'),
    path('<int:pk>/', ComplementsDetailView.as_view(), name='complements-detail'),
]
