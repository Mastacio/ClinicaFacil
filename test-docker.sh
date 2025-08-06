#!/bin/bash

# Script para probar la construcción y ejecución de la imagen Docker
# Uso: ./test-docker.sh

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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

print_step "=== PRUEBA DE CONSTRUCCIÓN Y EJECUCIÓN DOCKER ==="

# Limpiar imágenes anteriores de prueba
print_message "Limpiando imágenes de prueba anteriores..."
docker rmi clinica-facil:test 2>/dev/null || true

# Construir imagen de prueba
print_step "Construyendo imagen de prueba..."
if docker build -t clinica-facil:test .; then
    print_success "✅ Imagen construida exitosamente!"
else
    print_error "❌ Error al construir la imagen"
    exit 1
fi

# Verificar que la imagen existe
print_step "Verificando imagen creada..."
if docker images clinica-facil:test | grep -q clinica-facil; then
    print_success "✅ Imagen verificada correctamente"
    docker images clinica-facil:test
else
    print_error "❌ La imagen no se creó correctamente"
    exit 1
fi

# Probar ejecución del contenedor
print_step "Probando ejecución del contenedor..."
CONTAINER_ID=$(docker run -d -p 8000:8000 clinica-facil:test)

if [ $? -eq 0 ]; then
    print_success "✅ Contenedor iniciado correctamente"
    print_message "ID del contenedor: $CONTAINER_ID"
    
    # Esperar un momento para que el contenedor se inicie
    print_message "Esperando que el contenedor se inicie..."
    sleep 5
    
    # Verificar que el contenedor esté ejecutándose
    if docker ps | grep -q $CONTAINER_ID; then
        print_success "✅ Contenedor ejecutándose correctamente"
        
        # Verificar logs
        print_step "Verificando logs del contenedor..."
        docker logs $CONTAINER_ID
        
        # Probar conexión HTTP (opcional)
        print_step "Probando conexión HTTP..."
        if curl -s http://localhost:8000 > /dev/null 2>&1; then
            print_success "✅ Aplicación respondiendo en http://localhost:8000"
        else
            print_warning "⚠️  La aplicación no responde aún (puede estar iniciando)"
        fi
        
        # Detener contenedor
        print_step "Deteniendo contenedor de prueba..."
        docker stop $CONTAINER_ID
        docker rm $CONTAINER_ID
        print_success "✅ Contenedor detenido y eliminado"
        
    else
        print_error "❌ El contenedor no se está ejecutando"
        docker logs $CONTAINER_ID
        docker stop $CONTAINER_ID 2>/dev/null || true
        docker rm $CONTAINER_ID 2>/dev/null || true
        exit 1
    fi
else
    print_error "❌ Error al iniciar el contenedor"
    exit 1
fi

print_step "=== PRUEBA COMPLETADA ==="
print_success "🎉 Todas las pruebas pasaron correctamente!"
print_message "La imagen Docker está lista para usar"
print_message "Puedes ejecutar: ./docker-build-push.sh para hacer push" 