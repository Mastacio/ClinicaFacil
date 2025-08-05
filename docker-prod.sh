#!/bin/bash

# Script para construir y hacer push de la imagen de producción
# Uso: ./docker-prod.sh [nombre-imagen] [tag]

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
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
DEFAULT_TAG="prod"

# Obtener parámetros
IMAGE_NAME=${1:-$DEFAULT_IMAGE_NAME}
TAG=${2:-$DEFAULT_TAG}

# Construir el nombre completo de la imagen
FULL_IMAGE_NAME="$IMAGE_NAME:$TAG"

print_step "=== CONSTRUCCIÓN DE IMAGEN DE PRODUCCIÓN ==="
print_message "Nombre de imagen: $FULL_IMAGE_NAME"
print_message "Usando Dockerfile.prod para optimización de producción"

# Construir la imagen de producción
print_step "Construyendo imagen de producción..."
if docker build -f Dockerfile.prod -t "$FULL_IMAGE_NAME" .; then
    print_message "✅ Imagen de producción construida exitosamente!"
else
    print_error "❌ Error al construir la imagen de producción"
    exit 1
fi

# Mostrar información de la imagen
print_step "Información de la imagen:"
docker images "$FULL_IMAGE_NAME"

# Preguntar si hacer push
echo
read -p "¿Quieres hacer push de la imagen de producción a Docker Hub? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Haciendo push de la imagen de producción..."
    
    # Intentar hacer push
    if docker push "$FULL_IMAGE_NAME"; then
        print_message "✅ Push completado exitosamente!"
        print_message "🎉 Tu imagen de producción está disponible en: $FULL_IMAGE_NAME"
        
        # Mostrar comandos de uso
        echo
        print_step "Comandos útiles para usar la imagen:"
        echo "docker run -p 8000:8000 $FULL_IMAGE_NAME"
        echo "docker run -d -p 8000:8000 --name clinica-prod $FULL_IMAGE_NAME"
        echo "docker logs clinica-prod"
    else
        print_error "❌ Error al hacer push de la imagen"
        print_warning "Asegúrate de estar logueado en Docker Hub con 'docker login'"
        exit 1
    fi
else
    print_message "Push cancelado. La imagen está disponible localmente como: $FULL_IMAGE_NAME"
fi

print_step "=== PROCESO COMPLETADO ==="
print_message "La imagen de producción está lista para usar" 