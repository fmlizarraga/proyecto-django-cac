#!/bin/bash

# Directorio del proyecto
PROJECT_DIR="vinos"

# Verificar si el archivo requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "Error: El archivo requirements.txt no existe."
    exit 1
fi

# Instalar las dependencias necesarias
echo "Instalando dependencias..."
pip install -r requirements.txt

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

cd ../

