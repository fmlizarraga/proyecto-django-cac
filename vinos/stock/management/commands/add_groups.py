from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from stock.models import Branch, Employee, Product, Record

class Command(BaseCommand):
    help = 'Crear grupos y asignar permisos'

    def handle(self, *args, **options):
        group_admins, created = Group.objects.get_or_create(name='System admins')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "System admins" creado.'))
        else:
            self.stdout.write(f'El grupo "System admins" ya existe.')
        
        group_managers, created = Group.objects.get_or_create(name='Managers')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "Managers" creado.'))
        else:
            self.stdout.write(f'El grupo "Managers" ya existe.')

        group_bmanagers, created = Group.objects.get_or_create(name='Branch managers')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "Branch managers" creado.'))
        else:
            self.stdout.write(f'El grupo "Branch managers" ya existe.')

        group_workers, created = Group.objects.get_or_create(name='Workers')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "Workers" creado.'))
        else:
            self.stdout.write(f'El grupo "Workers" ya existe.')

        content_types = {
            'branch': ContentType.objects.get_for_model(Branch),
            'product': ContentType.objects.get_for_model(Product),
            'record': ContentType.objects.get_for_model(Record),
            'employee': ContentType.objects.get_for_model(Employee),
        }

        permissions = {
            'view_branch': Permission.objects.get(codename='view_branch', content_type=content_types['branch']),
            'add_branch': Permission.objects.get(codename='add_branch', content_type=content_types['branch']),
            'change_branch': Permission.objects.get(codename='change_branch', content_type=content_types['branch']),
            'delete_branch': Permission.objects.get(codename='delete_branch', content_type=content_types['branch']),
            
            'view_product': Permission.objects.get(codename='view_product', content_type=content_types['product']),
            'add_product': Permission.objects.get(codename='add_product', content_type=content_types['product']),
            'change_product': Permission.objects.get(codename='change_product', content_type=content_types['product']),
            'delete_product': Permission.objects.get(codename='delete_product', content_type=content_types['product']),
            
            'view_record': Permission.objects.get(codename='view_record', content_type=content_types['record']),
            'add_record': Permission.objects.get(codename='add_record', content_type=content_types['record']),
            'change_record': Permission.objects.get(codename='change_record', content_type=content_types['record']),
            'delete_record': Permission.objects.get(codename='delete_record', content_type=content_types['record']),

            'view_employee': Permission.objects.get(codename='view_employee', content_type=content_types['employee']),
            'add_employee': Permission.objects.get(codename='add_employee', content_type=content_types['employee']),
            'change_employee': Permission.objects.get(codename='change_employee', content_type=content_types['employee']),
            'delete_employee': Permission.objects.get(codename='delete_employee', content_type=content_types['employee']),
        }

        # Permisos de Admins
        group_admins.permissions.set(permissions.values())
        self.stdout.write(self.style.SUCCESS(f'Permisos agregados a grupo "System admins".'))

        # Permisos de Gerentes
        group_managers.permissions.set([
            permissions['view_branch'],
            permissions['change_branch'],
            permissions['view_product'],
            permissions['add_product'],
            permissions['view_record'],
            permissions['change_product'],
            permissions['view_employee'],
            permissions['add_employee'],
            permissions['change_employee'],
            permissions['delete_employee'],
        ])
        self.stdout.write(self.style.SUCCESS(f'Permisos agregados a grupo "Managers".'))

        # Permisos de Gerentes de sucursal
        group_bmanagers.permissions.set([
            permissions['view_branch'],
            permissions['view_product'],
            permissions['view_record'],
            permissions['add_record'],
            permissions['change_record'],
            permissions['delete_record'],
            permissions['view_employee'],
            permissions['add_employee'],
            permissions['change_employee'],
            permissions['delete_employee'],
        ])
        self.stdout.write(self.style.SUCCESS(f'Permisos agregados a grupo "Branch managers".'))

        # Permisos de trabajadores
        group_workers.permissions.set([
            permissions['view_branch'],
            permissions['view_product'],
            permissions['view_record'],
            permissions['add_record'],
            permissions['change_record'],
            permissions['view_employee'],
        ])
        self.stdout.write(self.style.SUCCESS(f'Permisos agregados a grupo "Workers".'))
