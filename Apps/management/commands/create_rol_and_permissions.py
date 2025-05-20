from ...Usuario.models import CustomPermission, Role
from django.core.management.base import BaseCommand

# Define todos los permisos base
perm_data = {
    "Client": ["add", "change", "delete", "view"],
    "ClientService": ["add", "change", "delete", "view"],
    "User": ["add", "change", "delete", "view"],
    "Services": ["add", "change", "delete", "view"],
    "PaymentHistory": ["change", "delete", "view"],
    "Role": ["add", "change", "delete", "view"],
    "CustomPermission": ["add", "change", "delete", "view"],
    "TributaryAdd": ["add", "change", "delete", "view"],
    "UserClientAssignment": ["add", "change", "delete", "view"],

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

        additional_codes = [
            "add_role", "change_role", "delete_role", "view_role",
            "add_custompermission", "change_custompermission", "delete_custompermission", "view_custompermission",
            "add_tributaryadd", "change_tributaryadd", "delete_tributaryadd", "view_tributaryadd",
            "add_userclientassignment", "change_userclientassignment", "delete_userclientassignment", "view_userclientassignment"
        ]
        perms_additional = CustomPermission.objects.filter(code__in=additional_codes)
        # Asignar permisos por rol
        all_permissions = CustomPermission.objects.all()

        # SuperAdmin → todos
        roles["Super Admin"].permissions.set(all_permissions)

        # Admin → todos menos los que empiezan con 'eliminar_'
        admin_perms_base = all_permissions.exclude(code__startswith="delete_")
        admin_perms = list(set(admin_perms_base + list(perms_additional)))
        roles["Admin"].permissions.set(admin_perms)

        # Colaborador → solo los que empiezan con 'ver_'
        colab_perms_base = all_permissions.filter(code__startswith="view_")
        colab_perms = list(set(colab_perms_base + list(perms_additional)))
        roles["Colaborador"].permissions.set(colab_perms)

        # Cliente → puede ver y editar clientes, ver clientService, users y paymentHistory
        cliente_codes_base = [
            "view_client", "change_client",
            "view_clientservice",
            "view_user",
            "view_paymenthistory"
        ]
        cliente_codes = cliente_codes_base + perms_additional
        cliente_perms = CustomPermission.objects.filter(code__in=cliente_codes)
        roles["Cliente"].permissions.set(cliente_perms)

        # Cliente Aux → puede ver clientes, clientService, users y services
        cliente_aux_codes_base = [
            "view_client",
            "view_clientservice",
            "view_user",
            "view_services"
        ]
        cliente_aux_codes = cliente_aux_codes_base + perms_additional
        cliente_aux_perms = CustomPermission.objects.filter(code__in=cliente_aux_codes)
        roles["Cliente Aux"].permissions.set(cliente_aux_perms)
