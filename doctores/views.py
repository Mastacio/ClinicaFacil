
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import HorarioDoctorForm, ConsultorioForm
from .models import DoctorPerfil, Especialidad, HorarioDoctor, Consultorio
from users.decorators import (
    admin_required, staff_required, role_required
)
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CrearDoctorForm

# Vistas para Consultorios
@role_required(['admin', 'asistente'])
def gestionar_consultorios(request):
    nombre = request.GET.get('nombre', '').strip()
    ubicacion = request.GET.get('ubicacion', '').strip()
    consultorios = Consultorio.objects.all()
    
    if nombre:
        consultorios = consultorios.filter(nombre__icontains=nombre)
    if ubicacion:
        consultorios = consultorios.filter(ubicacion__icontains=ubicacion)
    
    consultorios = consultorios.order_by('nombre')
    paginator = Paginator(consultorios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'doctores/gestionar_consultorios.html', {
        'page_obj': page_obj,
        'nombre': nombre,
        'ubicacion': ubicacion,
    })

@admin_required
def crear_consultorio(request):
    if request.method == 'POST':
        form = ConsultorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consultorio creado correctamente.')
            return redirect('gestionar_consultorios')
    else:
        form = ConsultorioForm()
    
    return render(request, 'doctores/crear_consultorio.html', {'form': form})

@role_required(['admin', 'asistente'])
def ver_consultorio(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    doctores_activos = consultorio.get_doctores_activos()
    horarios_activos = consultorio.get_horarios_activos()
    
    return render(request, 'doctores/ver_consultorio.html', {
        'consultorio': consultorio,
        'doctores_activos': doctores_activos,
        'horarios_activos': horarios_activos,
    })

@admin_required
def editar_consultorio(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    if request.method == 'POST':
        form = ConsultorioForm(request.POST, instance=consultorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consultorio actualizado correctamente.')
            return redirect('gestionar_consultorios')
    else:
        form = ConsultorioForm(instance=consultorio)
    
    return render(request, 'doctores/editar_consultorio.html', {'form': form, 'consultorio': consultorio})

@admin_required
def activar_desactivar_consultorio(request, pk):
    consultorio = get_object_or_404(Consultorio, pk=pk)
    consultorio.activo = not consultorio.activo
    consultorio.save()
    
    if consultorio.activo:
        messages.success(request, 'Consultorio activado correctamente.')
    else:
        messages.success(request, 'Consultorio desactivado correctamente.')
    
    return redirect('gestionar_consultorios')

# Vistas actualizadas para Horarios
@admin_required
def agregar_horario(request, pk):
    doctor = get_object_or_404(DoctorPerfil, pk=pk)
    if request.method == 'POST':
        form = HorarioDoctorForm(request.POST)
        if form.is_valid():
            try:
                horario = form.save(commit=False)
                horario.doctor = doctor
                horario.full_clean()  # Validar el modelo
                horario.save()
                messages.success(request, 'Horario agregado correctamente.')
                return redirect(reverse('ver_doctor', args=[doctor.pk]))
            except Exception as e:
                messages.error(request, f'Error al crear horario: {str(e)}')
    else:
        form = HorarioDoctorForm()
    
    return render(request, 'doctores/agregar_horario.html', {'form': form, 'doctor': doctor})

# Eliminar horario de un doctor (solo admin)
@admin_required
def eliminar_horario(request, doctor_pk, horario_pk):
    doctor = get_object_or_404(DoctorPerfil, pk=doctor_pk)
    horario = get_object_or_404(doctor.horarios, pk=horario_pk)
    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horario eliminado correctamente.')
        return redirect(reverse('ver_doctor', args=[doctor.pk]))
    return render(request, 'doctores/eliminar_horario.html', {'horario': horario, 'doctor': doctor})

# Vista para ver doctor
@role_required(['admin', 'asistente'])
def ver_doctor(request, pk):
    doctor = get_object_or_404(DoctorPerfil, pk=pk)
    return render(request, 'doctores/ver_doctor.html', {'doctor': doctor})

# Vista para editar doctor (solo admin)
@admin_required
def editar_doctor(request, pk):
    doctor = get_object_or_404(DoctorPerfil, pk=pk)
    if request.method == 'POST':
        form = CrearDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor actualizado correctamente.')
            return redirect('gestionar_doctores')
    else:
        form = CrearDoctorForm(instance=doctor)
    return render(request, 'doctores/editar_doctor.html', {'form': form, 'doctor': doctor})

# Vista para activar/desactivar doctor (solo admin)
@admin_required
def activar_desactivar_doctor(request, pk):
    doctor = get_object_or_404(DoctorPerfil, pk=pk)
    doctor.activo = not doctor.activo
    doctor.user.is_active = doctor.activo
    doctor.user.save()
    doctor.save()
    if doctor.activo:
        messages.success(request, 'Doctor activado correctamente.')
    else:
        messages.success(request, 'Doctor desactivado correctamente.')
    return redirect('gestionar_doctores')

@role_required(['admin', 'asistente'])
def gestionar_doctores(request):
    especialidad = request.GET.get('especialidad', '')
    nombre = request.GET.get('nombre', '').strip()
    identificacion = request.GET.get('identificacion', '').strip()
    doctores = DoctorPerfil.objects.select_related('user').all()
    if especialidad:
        doctores = doctores.filter(especialidades__id=especialidad)
    if nombre:
        doctores = doctores.filter(Q(user__first_name__icontains=nombre) | Q(user__last_name__icontains=nombre))
    if identificacion:
        doctores = doctores.filter(identificacion__icontains=identificacion)
    doctores = doctores.order_by('-id').distinct()
    paginator = Paginator(doctores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    especialidades = Especialidad.objects.all()
    return render(request, 'doctores/gestionar_doctores.html', {
        'page_obj': page_obj,
        'especialidades': especialidades,
        'especialidad': especialidad,
        'nombre': nombre,
        'identificacion': identificacion,
    })

@admin_required
def crear_doctor(request):
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, 'No tienes permisos para crear doctores.')
        return redirect('gestionar_doctores')
    if request.method == 'POST':
        form = CrearDoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor creado correctamente. Contraseña inicial: 12345678')
            return redirect('gestionar_doctores')
    else:
        form = CrearDoctorForm()
    return render(request, 'doctores/crear_doctor.html', {'form': form})
