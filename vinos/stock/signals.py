from django.db.models.signals import post_migrate
from django.apps import AppConfig
from django.db import connection

def handle_post_migrate(sender, **kwargs):
    if sender.name == 'stock':
        from django.core.management import call_command
        call_command('add_groups')
        call_command('add_users')

post_migrate.connect(handle_post_migrate, sender=AppConfig)
