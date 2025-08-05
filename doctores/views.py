
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import HorarioDoctorForm
from users.decorators import (
    admin_required, staff_required, role_required
)

@admin_required
def agregar_horario(request, pk):
    doctor = get_object_or_404(DoctorPerfil, pk=pk)
    if request.method == 'POST':
        form = HorarioDoctorForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.doctor = doctor
            horario.save()
            messages.success(request, 'Horario agregado correctamente.')
            return redirect(reverse('ver_doctor', args=[doctor.pk]))
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorPerfil, Especialidad
from .forms import CrearDoctorForm
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import User

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
