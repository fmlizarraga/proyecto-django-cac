from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Añade usuarios a grupos específicos después de las migraciones.'

    def handle(self, *args, **kwargs):
        try:
            user1 = User.objects.get(username='empleado1')
            user2 = User.objects.get(username='empleado2')

            bmanagers = Group.objects.get(name='System admins')
            workers = Group.objects.get(name='Workers')

            bmanagers.user_set.add(user1)
            workers.user_set.add(user2)

            self.stdout.write(self.style.SUCCESS('Usuarios añadidos a grupos correctamente.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No se encontró uno o más usuarios.'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('No se encontró uno o más grupos.'))
