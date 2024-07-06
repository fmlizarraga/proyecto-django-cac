# Proyecto Django CAC

Proyecto para el curso de backend con Django de Codo a Codo.

## Temática

Este proyecto es un sistema de control de stock para una bodega de vinos. Permite:
- Ver el inventario actual.
- Consultar productos (vinos) con sus respectivos datos.
- Realizar entradas y salidas de inventario.

## Requisitos

- Python 3.8 o superior.
- pip (gestor de paquetes de Python).
- Un entorno virtual para aislar las dependencias del proyecto.

## Pruebalo online!

https://proyecto-django-cac.onrender.com/

## Instalación y Configuración

### 1. Crear y activar el entorno virtual

Primero, crea un entorno virtual y actívalo. Esto garantiza que las dependencias del proyecto no interfieran con otros proyectos en tu máquina.

```sh
python3 -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### 2. Instalar dependencias

Instala todas las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

### 3. Aplicar migraciones

Ejecuta las migraciones para configurar la base de datos:

```sh
python manage.py migrate
```
### 4. Configurar las variables de entorno

Copiar el archivo env.template como .env y configurar las variables

SECRET_KEY: una clave utilizada por Djnago, asegurate de que sea segur y no la cmpartas.

DATABASE_URL: La URL de la base de datos de PostgreSQL

STATIC_URL: La url a la que se reidirigen las peticiones de archivos estaticos, normalmente '/static/' a menos que quieras configurar un servidor externo.

STATIC_ROOT: El directorio en el que se recolectan los archivos estaticos.

STATICFILES_EXTRA: Un directorio con archivos estaticos extra que no estan vinculados a una app especifica en el proyecto de Django.

### 5. Iniciar el servidor

Para iniciar el servidor de desarrollo, usa el siguiente comando dentro del directorio `vinos`:

```sh
cd vinos/
python manage.py runserver  # Agrega un número al final para cambiar el puerto, por ejemplo: `python manage.py runserver 8080`
```

## Tambien disponible en forma de contenedor de Docker

Solo clona el proyecto y abre una consola en la carpeta.

No olvides configurar los archivos del entorno

### .env
POSTGRES_PASSWORD: la contraseña del usuario de la base de datos

### .evn.production
SECRET_KEY: una clave utilizada por Djnago, asegurate de que sea segur y no la cmpartas.

DATABASE_URL: 'postgres://stockvinos_user:[reemplaza esta parte por la clave en POSTGRES_PASSWORD]@db/stockvinos'

STATIC_URL: '/static/'

STATIC_ROOT: '/app/static'

STATICFILES_EXTRA: '/app/static_extra'


### Ejecuta este comando para construir la imagen

```bash
docker-compose build
```

### Y para iniciar el servidor

```bash
docker-compose up
```

Se pude detener con CTRL + C o con

```bash
docker-compose down
```

### Tambien disponible en docker hub

https://hub.docker.com/r/fmlizarraga/proyecto-django-cac

Descargar con
```bash
docker pull fmlizarraga/proyecto-django-cac
```

## Datos Iniciales

Las migraciones crean algunos datos iniciales en la base de datos para facilitar las pruebas. Puedes usar los siguientes usuarios para iniciar sesión:

- **Usuario 1:**
  - Nombre de usuario: `empleado1`
  - Contraseña: `password1`

- **Usuario 2:**
  - Nombre de usuario: `empleado2`
  - Contraseña: `password2`

## Script de Inicio (Opcional)

Si estás en macOS, Linux o WSL, puedes usar el script `start.sh` para simplificar los pasos anteriores:

```sh
./start.sh [puerto] [ip(opcional)]
```

- El script hará lo siguiente:
  - Crear y activar un entorno virtual si no existe.
  - Instalar las dependencias listadas en `requirements.txt`.
  - Aplicar las migraciones de la base de datos.
  - Realizar la recoleccion de archivos estaticos en el directorio especificado en el entorno.
  - Iniciar el servidor Django en el puerto especificado (o en el puerto 8000 por defecto).

Ejemplo para iniciar el servidor en el puerto 8080:

```sh
./start.sh 8080
```

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Empuja tus cambios a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.