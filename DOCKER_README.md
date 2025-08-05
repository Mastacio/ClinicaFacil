# Docker Setup para ClínicaFacil

Este documento explica cómo configurar y usar Docker para la aplicación ClínicaFacil.

## Archivos de Docker

- `Dockerfile`: Configuración de la imagen Docker
- `docker-compose.yml`: Configuración para desarrollo con múltiples servicios
- `requirements.txt`: Dependencias de Python
- `.dockerignore`: Archivos excluidos del contexto de Docker
- `docker-build-push.sh`: Script automatizado para build y push

## Requisitos Previos

1. **Docker instalado**: [Instalar Docker](https://docs.docker.com/get-docker/)
2. **Docker Hub account**: [Crear cuenta](https://hub.docker.com/)

## Configuración Inicial

### 1. Login a Docker Hub

```bash
docker login
```

### 2. Verificar instalación

```bash
docker --version
docker-compose --version
```

## Uso Rápido

### Construir y hacer push de la imagen

```bash
# Usar el script automatizado
./docker-build-push.sh

# O especificar nombre y tag
./docker-build-push.sh mi-usuario/clinica-facil v1.0.0
```

### Desarrollo local con Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Comandos Docker manuales

```bash
# Construir imagen
docker build -t clinica-facil:latest .

# Ejecutar contenedor
docker run -p 8000:8000 clinica-facil:latest

# Hacer push a Docker Hub
docker tag clinica-facil:latest tu-usuario/clinica-facil:latest
docker push tu-usuario/clinica-facil:latest
```

## Estructura de la Imagen

```
/app/
├── manage.py
├── core/
├── citas/
├── doctores/
├── pacientes/
├── users/
├── gestion/
├── static/
└── requirements.txt
```

## Variables de Entorno

### Desarrollo
```bash
DEBUG=True
DJANGO_SETTINGS_MODULE=core.settings
```

### Producción
```bash
DEBUG=False
DJANGO_SETTINGS_MODULE=core.settings
DATABASE_URL=postgresql://user:password@host:port/db
SECRET_KEY=your-secret-key
```

## Puertos

- **8000**: Aplicación Django
- **5432**: Base de datos PostgreSQL (solo en desarrollo)

## Volúmenes

- `postgres_data`: Datos de PostgreSQL
- `static_volume`: Archivos estáticos
- `media_volume`: Archivos de media

## Troubleshooting

### Error de permisos
```bash
sudo usermod -aG docker $USER
# Reiniciar sesión
```

### Error de puerto ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"
```

### Limpiar Docker
```bash
# Eliminar contenedores no usados
docker container prune

# Eliminar imágenes no usadas
docker image prune

# Eliminar todo (cuidado)
docker system prune -a
```

## Comandos Útiles

```bash
# Ver imágenes locales
docker images

# Ver contenedores ejecutándose
docker ps

# Ver logs de un contenedor
docker logs <container_id>

# Ejecutar comando en contenedor
docker exec -it <container_id> bash

# Copiar archivos del contenedor
docker cp <container_id>:/app/file.txt ./
```

## Despliegue en Producción

1. **Construir imagen de producción**:
```bash
docker build -t clinica-facil:prod .
```

2. **Configurar variables de entorno**:
```bash
export DJANGO_SETTINGS_MODULE=core.settings
export DEBUG=False
export SECRET_KEY=your-secret-key
```

3. **Ejecutar con Gunicorn**:
```bash
docker run -p 8000:8000 -e DJANGO_SETTINGS_MODULE=core.settings clinica-facil:prod
```

## Seguridad

- La imagen usa un usuario no-root (`appuser`)
- Se excluyen archivos sensibles con `.dockerignore`
- Las variables de entorno se configuran externamente
- Se recomienda usar secrets en producción

## Contribuir

1. Modifica el `Dockerfile` según necesidades
2. Actualiza `requirements.txt` si agregas dependencias
3. Prueba con `docker-compose up --build`
4. Haz push de la nueva imagen 