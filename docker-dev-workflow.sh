#!/bin/bash

# Script para automatizar el flujo de desarrollo con Docker
# Incluye build, push, pull y ejecución de la imagen de desarrollo
# Uso: ./docker-dev-workflow.sh [acción] [usuario] [tag]

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_dev() {
    echo -e "${PURPLE}[DEV]${NC} $1"
}

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

# Configuración por defecto
ACTION=${1:-"help"}
DOCKER_USER=${2:-"clinica-facil"}
TAG=${3:-"dev"}

# Construir el nombre completo de la imagen
FULL_IMAGE_NAME="$DOCKER_USER:$TAG"

# Función para mostrar ayuda
show_help() {
    echo "Uso: ./docker-dev-workflow.sh [acción] [usuario] [tag]"
    echo ""
    echo "ACCIONES:"
    echo "  build     - Construir imagen de desarrollo"
    echo "  push      - Hacer push de la imagen"
    echo "  pull      - Hacer pull de la imagen"
    echo "  run       - Ejecutar contenedor de desarrollo"
    echo "  run-db    - Ejecutar con base de datos"
    echo "  update    - Build + Push (actualizar imagen)"
    echo "  deploy    - Pull + Run (desplegar en otro equipo)"
    echo "  clean     - Limpiar contenedores y imágenes"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "EJEMPLOS:"
    echo "  ./docker-dev-workflow.sh build mi-usuario dev"
    echo "  ./docker-dev-workflow.sh push mi-usuario dev"
    echo "  ./docker-dev-workflow.sh run mi-usuario dev"
    echo "  ./docker-dev-workflow.sh run-db mi-usuario dev"
    echo ""
    echo "CONFIGURACIÓN:"
    echo "  Usuario por defecto: clinica-facil"
    echo "  Tag por defecto: dev"
}

# Función para construir imagen
build_image() {
    print_step "=== CONSTRUYENDO IMAGEN DE DESARROLLO ==="
    print_message "Imagen: $FULL_IMAGE_NAME"
    
    if docker build -t "$FULL_IMAGE_NAME" .; then
        print_success "✅ Imagen construida exitosamente!"
        docker images "$FULL_IMAGE_NAME"
    else
        print_error "❌ Error al construir la imagen"
        exit 1
    fi
}

# Función para hacer push
push_image() {
    print_step "=== HACIENDO PUSH DE LA IMAGEN ==="
    print_message "Imagen: $FULL_IMAGE_NAME"
    
    # Verificar login
    if ! docker info &> /dev/null; then
        print_error "No estás logueado en Docker Hub"
        print_message "Ejecuta: docker login"
        exit 1
    fi
    
    if docker push "$FULL_IMAGE_NAME"; then
        print_success "✅ Push completado exitosamente!"
        print_message "Imagen disponible en Docker Hub: $FULL_IMAGE_NAME"
    else
        print_error "❌ Error al hacer push"
        exit 1
    fi
}

# Función para hacer pull
pull_image() {
    print_step "=== HACIENDO PULL DE LA IMAGEN ==="
    print_message "Imagen: $FULL_IMAGE_NAME"
    
    if docker pull "$FULL_IMAGE_NAME"; then
        print_success "✅ Pull completado exitosamente!"
        docker images "$FULL_IMAGE_NAME"
    else
        print_error "❌ Error al hacer pull"
        exit 1
    fi
}

# Función para ejecutar contenedor
run_container() {
    print_step "=== EJECUTANDO CONTENEDOR DE DESARROLLO ==="
    print_message "Imagen: $FULL_IMAGE_NAME"
    
    # Detener contenedor existente si existe
    docker stop clinica-dev 2>/dev/null || true
    docker rm clinica-dev 2>/dev/null || true
    
    print_dev "Ejecutando en modo desarrollo..."
    print_dev "Puerto: 8000"
    print_dev "Variables de entorno: DEBUG=True"
    
    docker run -d -p 8000:8000 \
        -e DEBUG=True \
        -e DJANGO_SETTINGS_MODULE=core.settings \
        --name clinica-dev \
        "$FULL_IMAGE_NAME"
    
    if [ $? -eq 0 ]; then
        print_success "✅ Contenedor iniciado correctamente!"
        print_message "Aplicación disponible en: http://localhost:8000"
        print_message "Ver logs: docker logs -f clinica-dev"
        print_message "Detener: docker stop clinica-dev"
    else
        print_error "❌ Error al iniciar el contenedor"
        exit 1
    fi
}

# Función para ejecutar con base de datos
run_with_db() {
    print_step "=== EJECUTANDO CON BASE DE DATOS ==="
    print_message "Imagen: $FULL_IMAGE_NAME"
    
    # Crear red si no existe
    docker network create clinica-dev-network 2>/dev/null || true
    
    # Detener contenedores existentes
    docker stop clinica-dev clinica-db 2>/dev/null || true
    docker rm clinica-dev clinica-db 2>/dev/null || true
    
    print_dev "Iniciando base de datos PostgreSQL..."
    docker run -d \
        --name clinica-db \
        --network clinica-dev-network \
        -e POSTGRES_DB=clinica_facil \
        -e POSTGRES_USER=clinica_user \
        -e POSTGRES_PASSWORD=clinica_password \
        -p 5432:5432 \
        postgres:15
    
    if [ $? -eq 0 ]; then
        print_success "✅ Base de datos iniciada!"
        
        print_dev "Esperando que la BD esté lista..."
        sleep 10
        
        print_dev "Iniciando aplicación..."
        docker run -d -p 8000:8000 \
            --network clinica-dev-network \
            -e DEBUG=True \
            -e DJANGO_SETTINGS_MODULE=core.settings \
            -e DATABASE_URL=postgresql://clinica_user:clinica_password@clinica-db:5432/clinica_facil \
            --name clinica-dev \
            "$FULL_IMAGE_NAME"
        
        if [ $? -eq 0 ]; then
            print_success "✅ Aplicación iniciada con base de datos!"
            print_message "Aplicación: http://localhost:8000"
            print_message "Base de datos: localhost:5432"
            print_message "Ver logs: docker logs -f clinica-dev"
        else
            print_error "❌ Error al iniciar la aplicación"
            exit 1
        fi
    else
        print_error "❌ Error al iniciar la base de datos"
        exit 1
    fi
}

# Función para actualizar imagen
update_image() {
    print_step "=== ACTUALIZANDO IMAGEN ==="
    build_image
    push_image
}

# Función para desplegar en otro equipo
deploy_image() {
    print_step "=== DESPLEGANDO EN OTRO EQUIPO ==="
    pull_image
    run_container
}

# Función para limpiar
clean_all() {
    print_step "=== LIMPIANDO CONTENEDORES E IMÁGENES ==="
    
    # Detener y eliminar contenedores
    docker stop clinica-dev clinica-db 2>/dev/null || true
    docker rm clinica-dev clinica-db 2>/dev/null || true
    
    # Eliminar imágenes
    docker rmi "$FULL_IMAGE_NAME" 2>/dev/null || true
    
    # Limpiar recursos no usados
    docker system prune -f
    
    print_success "✅ Limpieza completada!"
}

# Procesar acción
case $ACTION in
    "build")
        build_image
        ;;
    "push")
        push_image
        ;;
    "pull")
        pull_image
        ;;
    "run")
        run_container
        ;;
    "run-db")
        run_with_db
        ;;
    "update")
        update_image
        ;;
    "deploy")
        deploy_image
        ;;
    "clean")
        clean_all
        ;;
    "help"|*)
        show_help
        ;;
esac

print_step "=== PROCESO COMPLETADO ===" 