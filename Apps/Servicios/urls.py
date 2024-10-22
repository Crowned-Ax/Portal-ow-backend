from django.urls import path, include
from .views import ServicesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'services', ServicesViewSet, basename="services")

urlpatterns = [
    path('', include(router.urls)),
]
