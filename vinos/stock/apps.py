from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .signals import handle_post_migrate


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'

    def ready(self):
        post_migrate.connect(handle_post_migrate, sender=self)
