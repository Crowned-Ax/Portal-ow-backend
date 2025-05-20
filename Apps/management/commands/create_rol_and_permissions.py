from ...Usuario.models import CustomPermission, Role
from django.core.management.base import BaseCommand

# Define todos los permisos base
perm_data = {
    "Client": ["add", "change", "delete", "view"],
    "ClientService": ["add", "change", "delete", "view"],
    "User": ["add", "change", "delete", "view"],
    "Services": ["add", "change", "delete", "view"],
    "PaymentHistory": ["change", "delete", "view"],
    "Role": ["change", "delete", "view"],
    "CustomPermission": ["change", "delete", "view"],
    "TributaryAdd": ["change", "delete", "view"],
    "UserClientAssignment": ["change", "delete", "view"],

}

perm_data_names = {
    "Client": "Cliente",
    "ClientService": "ServiciosWordpress",
    "User": "Colaboradores",
    "Services": "Servicios",
    "PaymentHistory": "Pagos",
    "Role": "Roles",
    "CustomPermission": "Permisos",
    "TributaryAdd": "Tributaria",
    "UserClientAssignment": "Asignacion"
}

class Command(BaseCommand):
    help = "Crea usuarios para clientes existentes que aún no tienen usuario"

    def handle(self, *args, **kwargs):
        # Crea los permisos si no existen
        for model, actions in perm_data.items():
            name = perm_data_names[model]
            for action in actions:
                code = f"{action.lower()}_{model.lower()}"
                CustomPermission.objects.get_or_create(code=code, model=name)
        # Personalizado
        #CustomPermission.objects.get_or_create(code="view_client_own")
        # Crea los roles si no existen
        role_names = ["Super Admin", "Admin", "Colaborador", "Cliente", "Cliente Aux"]
        default_staff = [True, True, True, False, False]
        roles = {}
        for name, is_staff in zip(role_names, default_staff):
            role, _ = Role.objects.get_or_create(name=name, defaults={'is_staff': is_staff})
            roles[name] = role

        # Asignar permisos por rol
        all_permissions = CustomPermission.objects.all()

        # SuperAdmin → todos
        roles["Super Admin"].permissions.set(all_permissions)

        # Admin → todos menos los que empiezan con 'eliminar_'
        admin_perms = all_permissions.exclude(code__startswith="delete_")
        roles["Admin"].permissions.set(admin_perms)

        # Colaborador → solo los que empiezan con 'ver_'
        colab_perms = all_permissions.filter(code__startswith="view_")
        roles["Colaborador"].permissions.set(colab_perms)

        # Cliente → puede ver y editar clientes, ver clientService, users y paymentHistory
        cliente_codes = [
            "view_client", "change_client",
            "view_clientservice",
            "view_user",
            "view_paymenthistory"
        ]
        cliente_perms = CustomPermission.objects.filter(code__in=cliente_codes)
        roles["Cliente"].permissions.set(cliente_perms)

        # Cliente Aux → puede ver clientes, clientService, users y services
        cliente_aux_codes = [
            "view_client",
            "view_clientservice",
            "view_user",
            "view_services"
        ]
        cliente_aux_perms = CustomPermission.objects.filter(code__in=cliente_aux_codes)
        roles["Cliente Aux"].permissions.set(cliente_aux_perms)
