from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """Niega acceso solo a usuarios en el grupo 'Cliente'."""
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Cliente").exists()

class IsColaborator(BasePermission):
    """Niega acceso solo a usuarios en el grupo 'Colaborador'."""
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Colaborador").exists()

class IsClientAux(BasePermission):
    """Niega acceso solo a usuarios en el grupo 'ClienteAux'."""
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="ClienteAux").exists()
