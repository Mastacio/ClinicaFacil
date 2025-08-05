#!/bin/bash

# Script para construir y hacer push de la imagen Docker
# Uso: ./docker-build-push.sh [nombre-imagen] [tag]

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

# Verificar que el usuario esté logueado en Docker Hub
if ! docker info &> /dev/null; then
    print_error "No puedes acceder a Docker. Asegúrate de estar logueado con 'docker login'"
    exit 1
fi

# Configuración por defecto
DEFAULT_IMAGE_NAME="clinica-facil"
DEFAULT_TAG="latest"

# Obtener parámetros
IMAGE_NAME=${1:-$DEFAULT_IMAGE_NAME}
TAG=${2:-$DEFAULT_TAG}

# Construir el nombre completo de la imagen
FULL_IMAGE_NAME="$IMAGE_NAME:$TAG"

print_message "Iniciando construcción de imagen Docker..."
print_message "Nombre de imagen: $FULL_IMAGE_NAME"

# Construir la imagen
print_message "Construyendo imagen..."
if docker build -t "$FULL_IMAGE_NAME" .; then
    print_message "Imagen construida exitosamente!"
else
    print_error "Error al construir la imagen"
    exit 1
fi

# Preguntar si hacer push
read -p "¿Quieres hacer push de la imagen a Docker Hub? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_message "Haciendo push de la imagen..."
    
    # Intentar hacer push
    if docker push "$FULL_IMAGE_NAME"; then
        print_message "Push completado exitosamente!"
        print_message "Tu imagen está disponible en: $FULL_IMAGE_NAME"
    else
        print_error "Error al hacer push de la imagen"
        print_warning "Asegúrate de estar logueado en Docker Hub con 'docker login'"
        exit 1
    fi
else
    print_message "Push cancelado. La imagen está disponible localmente como: $FULL_IMAGE_NAME"
fi

print_message "Proceso completado!" 