# vinos/create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinos.settings')
django.setup()

User = get_user_model()
SUPERUSER_NAME = os.getenv('DJANGO_SUPERUSER_NAME')
SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=SUPERUSER_NAME).exists():
    User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print('Superusuario creado exitosamente')
else:
    print('El superusuario ya existe')
