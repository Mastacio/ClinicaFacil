from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings


class RoleMiddleware:
    """
    Middleware para validar roles y permisos en tiempo real.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Procesar la solicitud
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Validar permisos antes de ejecutar la vista.
        """
        # Si el usuario no está autenticado, no hacer nada (Django manejará el login)
        if not request.user.is_authenticated:
            return None
        
        # URLs que no requieren validación de roles
        excluded_urls = [
            '/login/',
            '/logout/',
            '/registro/',
            '/panel/',
            '/welcome/',
            '/',
            '/static/',
            '/media/',
        ]
        
        # Verificar si la URL actual está excluida
        current_path = request.path
        for excluded_url in excluded_urls:
            if current_path.startswith(excluded_url):
                return None
        
        # Validar que el usuario tenga un rol asignado
        if not hasattr(request.user, 'role'):
            messages.error(request, 'Tu cuenta no tiene un rol asignado. Contacta al administrador.')
            return redirect('welcome')
        
        # Validaciones específicas por rol
        if request.user.role == 'paciente':
            # Pacientes no pueden acceder a vistas administrativas
            restricted_urls = [
                '/doctores/',
                '/gestion/',
                '/admin/',
            ]
            for restricted_url in restricted_urls:
                if current_path.startswith(restricted_url):
                    messages.error(request, 'No tienes permisos para acceder a esta sección.')
                    return redirect('welcome')
        
        elif request.user.role == 'doctor':
            # Doctores no pueden acceder a vistas de administración de usuarios
            restricted_urls = [
                '/admin/',
            ]
            for restricted_url in restricted_urls:
                if current_path.startswith(restricted_url):
                    messages.error(request, 'No tienes permisos para acceder a esta sección.')
                    return redirect('welcome')
        
        elif request.user.role == 'asistente':
            # Asistentes no pueden acceder a vistas de administración del sistema
            restricted_urls = [
                '/admin/',
            ]
            for restricted_url in restricted_urls:
                if current_path.startswith(restricted_url):
                    messages.error(request, 'No tienes permisos para acceder a esta sección.')
                    return redirect('welcome')
        
        return None 