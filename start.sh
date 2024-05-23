#!/bin/bash

# Nombre del entorno virtual
VENV_DIR="venv"

# Directorio del proyecto
PROJECT_DIR="vinos"

# Comando para crear el entorno virtual
CREATE_VENV_CMD="python3 -m venv $VENV_DIR"

# Comando para activar el entorno virtual
ACTIVATE_VENV_CMD="source $VENV_DIR/bin/activate"

# Verificar si el entorno virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "El entorno virtual no existe. Creándolo..."
    $CREATE_VENV_CMD

    # Instalar las dependencias necesarias
    $ACTIVATE_VENV_CMD
    pip install -r requirements.txt
fi

# Activar el entorno virtual
echo "Activando el entorno virtual..."
$ACTIVATE_VENV_CMD

# Cambiar al directorio del proyecto
echo "Cambiando al directorio del proyecto..."
cd $PROJECT_DIR

# Iniciar el servidor de Django
echo "Iniciando el servidor de Django..."
python manage.py runserver 8245
