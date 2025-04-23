from ...Usuario.models import CustomPermission, Role

# Define todos los permisos base
perm_data = {
    "Client": ["add", "change", "delete", "view"],
    "ClientService": ["add", "change", "delete", "view"],
    "User": ["add", "change", "delete", "view"],
    "Services": ["add", "change", "delete", "view"],
    "PaymentHistory": ["change", "delete", "view"]
}

# Crea los permisos si no existen
for model, actions in perm_data.items():
    for action in actions:
        code = f"{action.lower()}_{model.lower()}"
        CustomPermission.objects.get_or_create(code=code)
# Personalizado
#CustomPermission.objects.get_or_create(code="view_client_own")
# Crea los roles si no existen
role_names = ["SuperAdmin", "Admin", "Colaborador", "Cliente", "Cliente-Aux"]
roles = {}
for name in role_names:
    role, _ = Role.objects.get_or_create(name=name)
    roles[name] = role

# Asignar permisos por rol
all_permissions = CustomPermission.objects.all()

# SuperAdmin → todos
roles["SuperAdmin"].permissions.set(all_permissions)

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
