from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crea los roles y asigna permisos"

    def handle(self, *args, **kwargs):
        roles = ["Cliente", "Colaborador", "ClienteAux"]
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{role}' creado correctamente"))
            else:
                self.stdout.write(self.style.WARNING(f"Grupo '{role}' ya existe"))

        self.stdout.write(self.style.SUCCESS("✅ Roles configurados correctamente"))
