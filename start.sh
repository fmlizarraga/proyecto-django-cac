#!/bin/bash

# Nombre del entorno virtual
VENV_DIR="venv"

# Directorio del proyecto
PROJECT_DIR="vinos"

# Comando para crear el entorno virtual
CREATE_VENV_CMD="python3 -m venv $VENV_DIR"

# Comando para activar el entorno virtual
ACTIVATE_VENV_CMD="source $VENV_DIR/bin/activate"

# Puerto y host por defecto para el servidor Django
DEFAULT_PORT=8000
DEFAULT_HOST="127.0.0.1"

# Si se proporciona un puerto y/o host como argumento, usarlos
if [ $# -ge 1 ]; then
    PORT=$1
else
    PORT=$DEFAULT_PORT
fi

if [ $# -ge 2 ]; then
    HOST=$2
else
    HOST=$DEFAULT_HOST
fi

# Verificar si el entorno virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "El entorno virtual no existe. Creándolo..."
    $CREATE_VENV_CMD

    # Verificar si el entorno virtual se creó correctamente
    if [ $? -ne 0 ]; then
        echo "Error: No se pudo crear el entorno virtual."
        exit 1
    fi

    # Activar el entorno virtual
    echo "Activando el entorno virtual..."
    $ACTIVATE_VENV_CMD

    # Verificar si el archivo requirements.txt existe
    if [ ! -f "requirements.txt" ]; then
        echo "Error: El archivo requirements.txt no existe."
        exit 1
    fi

    # Instalar las dependencias necesarias
    echo "Instalando dependencias..."
    pip install -r requirements.txt

    # Verificar si la instalación de dependencias fue exitosa
    if [ $? -ne 0 ]; then
        echo "Error: No se pudieron instalar las dependencias."
        exit 1
    fi
else
    # Activar el entorno virtual
    echo "Activando el entorno virtual..."
    $ACTIVATE_VENV_CMD
fi

# Cambiar al directorio del proyecto
echo "Cambiando al directorio del proyecto..."
cd $PROJECT_DIR

# Aplicar las migraciones
echo "Aplicando migraciones de datos..."
python manage.py migrate

# Verificar si las migraciones se aplicaron correctamente
if [ $? -ne 0 ]; then
    echo "Error: No se pudieron aplicar las migraciones."
    exit 1
fi

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Verificar si la recopilación de archivos estáticos fue exitosa
if [ $? -ne 0 ]; then
    echo "Error: No se pudieron recopilar los archivos estáticos."
    exit 1
fi

# Iniciar el servidor de Django
echo "Iniciando el servidor de Django en $HOST:$PORT..."
python manage.py runserver $HOST:$PORT
