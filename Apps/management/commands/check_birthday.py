from django.core.management.base import BaseCommand
from datetime import date, timedelta
from django.utils.timezone import now
from Usuario.models import User
from Notificaciones.models import Notification

class Command(BaseCommand):
    help = 'Revisa cumpleaños próximos y crea/actualiza notificación tipo evento'

    def handle(self, *args, **kwargs):
        today = date.today()
        upcoming = today + timedelta(days=7)

        users_with_upcoming_birthdays = []

        for user in User.objects.all():
            if user.birthday:
                birthday_this_year = user.birthday.replace(year=today.year)
                if today <= birthday_this_year <= upcoming:
                    days_left = (birthday_this_year - today).days
                    if days_left == 0:
                        users_with_upcoming_birthdays.append(f"🎉 Hoy cumple {user.get_full_name()}")
                    else:
                        users_with_upcoming_birthdays.append(f"🎂 {user.get_full_name()} cumple en {days_left} días")

        if users_with_upcoming_birthdays:
            full_message = "Cumpleaños próximos:\n" + "\n".join(users_with_upcoming_birthdays)

            noti, created = Notification.objects.get_or_create(
                type='event',
                user=None,
                message__startswith="Cumpleaños próximos:"
            )

            noti.message = full_message
            noti.date = today
            noti.save()

            if created:
                self.stdout.write(self.style.SUCCESS('Notificación de cumpleaños creada.'))
            else:
                self.stdout.write(self.style.SUCCESS('Notificación de cumpleaños actualizada.'))
        else:
            self.stdout.write(self.style.WARNING('No hay cumpleaños próximos.'))
