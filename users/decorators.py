from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden


def role_required(allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos.
    
    Uso:
    @role_required(['admin', 'doctor'])
    def mi_vista(request):
        pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            if not hasattr(request.user, 'role'):
                messages.error(request, 'Tu cuenta no tiene un rol asignado.')
                return redirect('welcome')
            
            if request.user.role not in allowed_roles:
                messages.error(request, f'No tienes permisos para acceder a esta página. Tu rol actual es: {request.user.get_role_display()}')
                return redirect('welcome')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """
    Decorador para vistas que solo pueden acceder administradores.
    """
    return role_required(['admin'])(view_func)


def doctor_required(view_func):
    """
    Decorador para vistas que solo pueden acceder doctores.
    """
    return role_required(['admin', 'doctor'])(view_func)


def asistente_required(view_func):
    """
    Decorador para vistas que solo pueden acceder asistentes.
    """
    return role_required(['admin', 'asistente'])(view_func)


def paciente_required(view_func):
    """
    Decorador para vistas que solo pueden acceder pacientes.
    """
    return role_required(['paciente'])(view_func)


def staff_required(view_func):
    """
    Decorador para vistas que solo pueden acceder personal administrativo.
    """
    return role_required(['admin', 'doctor', 'asistente'])(view_func)


def owner_required(model_class, pk_name='pk'):
    """
    Decorador para verificar que el usuario sea dueño del objeto o tenga permisos administrativos.
    
    Uso:
    @owner_required(DoctorPerfil)
    def editar_doctor(request, pk):
        pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Administradores pueden acceder a todo
            if request.user.role == 'admin':
                return view_func(request, *args, **kwargs)
            
            # Obtener el objeto
            pk = kwargs.get(pk_name)
            if not pk:
                messages.error(request, 'ID de objeto no válido.')
                return redirect('welcome')
            
            try:
                obj = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                messages.error(request, 'El objeto solicitado no existe.')
                return redirect('welcome')
            
            # Verificar si el usuario es dueño del objeto
            if hasattr(obj, 'user') and obj.user == request.user:
                return view_func(request, *args, **kwargs)
            
            # Para doctores, verificar si es su perfil
            if request.user.role == 'doctor' and hasattr(obj, 'user') and obj.user == request.user:
                return view_func(request, *args, **kwargs)
            
            # Para pacientes, verificar si es su perfil
            if request.user.role == 'paciente' and hasattr(obj, 'user') and obj.user == request.user:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permisos para acceder a este recurso.')
            return redirect('welcome')
        
        return _wrapped_view
    return decorator


def cita_owner_required(view_func):
    """
    Decorador específico para verificar permisos en citas.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        from citas.models import Cita
        
        # Administradores pueden acceder a todo
        if request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        
        # Obtener la cita
        cita_id = kwargs.get('pk')
        if not cita_id:
            messages.error(request, 'ID de cita no válido.')
            return redirect('welcome')
        
        try:
            cita = Cita.objects.get(pk=cita_id)
        except Cita.DoesNotExist:
            messages.error(request, 'La cita solicitada no existe.')
            return redirect('welcome')
        
        # Verificar permisos según el rol
        if request.user.role == 'doctor':
            # Doctores solo pueden acceder a sus propias citas
            if cita.doctor.user == request.user:
                return view_func(request, *args, **kwargs)
        
        elif request.user.role == 'paciente':
            # Pacientes solo pueden acceder a sus propias citas
            if cita.paciente.user == request.user:
                return view_func(request, *args, **kwargs)
        
        elif request.user.role == 'asistente':
            # Asistentes pueden acceder a todas las citas
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'No tienes permisos para acceder a esta cita.')
        return redirect('welcome')
    
    return _wrapped_view 