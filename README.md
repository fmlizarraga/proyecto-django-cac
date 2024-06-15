# proyecto-django-cac
Proyecto para el curso de backend con Django de Codo a Codo

## Temática

Control de stock para una bodega de vinos, permite ver el inventario actual, productos (vinos) con sus respectivos datos y permite realizar entradas y salidas de inventario.

## Como iniciar el servidor

(todos estos pasos se pueden obviar si se usa start.sh en mac/linux/wsl)

Primero no olvides crear un entorno virtual y activarlo!
```
python3 -m venv venv
source venv/bin/activate
```
Instala Django (la unica dependencia por ahora)
```
pip install django
```
Inicia el servidor asi
```
cd vinos/
python manage.py runserver
```

## Admin superuser
- usuario: super
- contraseña: super45