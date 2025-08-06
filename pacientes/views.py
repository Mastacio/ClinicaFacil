# Importaciones necesarias para las vistas de pacientes
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PacientePerfil
from .forms import PacientePerfilForm
from users.decorators import (
    role_required, admin_required, doctor_required, staff_required
)
# Vista para ver paciente
@role_required(['admin', 'doctor'])
def ver_paciente(request, pk):
    from datetime import date
    paciente = get_object_or_404(PacientePerfil, pk=pk)
    edad = None
    if paciente.fecha_nacimiento:
        today = date.today()
        edad = today.year - paciente.fecha_nacimiento.year - (
            (today.month, today.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day)
        )
    return render(request, 'pacientes/ver_paciente.html', {'paciente': paciente, 'edad': edad})

# Vista para editar paciente
@role_required(['admin', 'doctor'])
def editar_paciente(request, pk):
    paciente = get_object_or_404(PacientePerfil, pk=pk)
    if request.method == 'POST':
        form = PacientePerfilForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('gestionar_pacientes')
    else:
        form = PacientePerfilForm(instance=paciente)
    return render(request, 'pacientes/editar_paciente.html', {'form': form, 'paciente': paciente})


# Vista para activar/desactivar paciente
@role_required(['admin', 'doctor'])
def activar_desactivar_paciente(request, pk):
    paciente = get_object_or_404(PacientePerfil, pk=pk)
    paciente.user.is_active = not paciente.user.is_active
    paciente.user.save()
    if paciente.user.is_active:
        messages.success(request, 'Paciente activado correctamente.')
    else:
        messages.success(request, 'Paciente desactivado correctamente.')
    return redirect('gestionar_pacientes')
from django.core.paginator import Paginator
from django.db.models import Q

@role_required(['admin', 'doctor'])
def gestionar_pacientes(request):
    nombre = request.GET.get('nombre', '').strip()
    identificacion = request.GET.get('identificacion', '').strip()
    pacientes = PacientePerfil.objects.select_related('user').all()
    if nombre:
        pacientes = pacientes.filter(Q(user__first_name__icontains=nombre) | Q(user__last_name__icontains=nombre))
    if identificacion:
        pacientes = pacientes.filter(identificacion__icontains=identificacion)
    pacientes = pacientes.order_by('-id')
    paginator = Paginator(pacientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pacientes/gestionar_pacientes.html', {
        'page_obj': page_obj,
        'nombre': nombre,
        'identificacion': identificacion,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PacientePerfil
from .forms import PacientePerfilForm, CrearPacienteForm

@role_required(['admin', 'doctor'])
def crear_paciente(request):
    if request.method == 'POST':
        user_form = CrearPacienteForm(request.POST)
        perfil_form = PacientePerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.completado = True
            perfil.save()
            messages.success(request, 'Paciente creado correctamente. Contraseña inicial: 12345678')
            return redirect('welcome')
    else:
        user_form = CrearPacienteForm()
        perfil_form = PacientePerfilForm()
    return render(request, 'pacientes/crear_paciente.html', {'user_form': user_form, 'perfil_form': perfil_form})
from django.contrib import messages

@login_required(login_url='/login/')
def completar_perfil(request):
    perfil, created = PacientePerfil.objects.get_or_create(user=request.user)
    if perfil.completado:
        messages.info(request, 'Tu perfil ya está completo.')
        return redirect('welcome')
    if request.method == 'POST':
        form = PacientePerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.completado = True
            perfil.save()
            messages.success(request, 'Perfil completado correctamente.')
            return redirect('welcome')
    else:
        form = PacientePerfilForm(instance=perfil)
    return render(request, 'pacientes/completar_perfil.html', {'form': form})
