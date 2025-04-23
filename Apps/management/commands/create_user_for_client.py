from django.core.management.base import BaseCommand
from ...Clientes.models import Client
from ...Usuario.models import User

class Command(BaseCommand):
    help = "Crea usuarios para clientes existentes que aún no tienen usuario"

    def handle(self, *args, **kwargs):
        clients_without_users = Client.objects.filter(user__isnull=True)

        for client in clients_without_users:
            user = User.objects.create_user(
                email=client.email,
                password=client.documentNumber
            )
            client.user = user
            client.save()

        self.stdout.write(self.style.SUCCESS(f"Usuarios creados para {clients_without_users.count()} clientes."))
