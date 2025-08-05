from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from citas.models import Cita
from .models import GestionCita, MedicamentoAsignado, AnalisisAsignado, Medicamento, Analisis, ConfiguracionImpresion
from .forms import GestionCitaForm, MedicamentoAsignadoForm, AnalisisAsignadoForm
from datetime import date
from users.decorators import (
    role_required, admin_required, doctor_required, staff_required
)

def construir_url_con_filtros(base_url, request):
    """
    Función auxiliar para construir URLs con filtros de agenda
    """
    params = []
    
    # Obtener filtros de GET y POST
    fecha = request.GET.get('fecha') or request.POST.get('fecha')
    estado = request.GET.get('estado') or request.POST.get('estado')
    paciente = request.GET.get('paciente') or request.POST.get('paciente')
    doctor = request.GET.get('doctor') or request.POST.get('doctor')
    
    if fecha:
        params.append(f"fecha={fecha}")
    if estado:
        params.append(f"estado={estado}")
    if paciente:
        params.append(f"paciente={paciente}")
    if doctor:
        params.append(f"doctor={doctor}")
    
    if params:
        base_url += '?' + '&'.join(params)
    
    return base_url

@role_required(['admin', 'doctor'])
def gestionar_cita(request, cita_id):
    """
    Vista para gestionar una cita específica
    """
    cita = get_object_or_404(Cita, pk=cita_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        # Admin puede gestionar cualquier cita
        pass
    elif cita.doctor.user != request.user:
        # Doctor solo puede gestionar sus propias citas
        messages.error(request, 'No tienes permisos para gestionar esta cita.')
        return redirect('agenda_doctor')
    
    # Obtener o crear la gestión
    gestion, created = GestionCita.objects.get_or_create(
        cita=cita,
        defaults={
            'paciente': cita.paciente,
            'doctor': cita.doctor,
            'motivo_consulta': cita.motivo,
            'creado_por': request.user
        }
    )
    
    # Inicializar el formulario
    if request.method == 'POST':
        form = GestionCitaForm(request.POST, instance=gestion)
        if form.is_valid():
            gestion = form.save(commit=False)
            gestion.creado_por = request.user
            gestion.save()
            messages.success(request, 'Gestión actualizada correctamente.')
            
            # Si el estado se cambió a completada, redirigir a la agenda con filtros
            if gestion.estado == 'completada':
                # También completar la cita asociada
                cita.estado = 'completada'
                cita.save()
                
                # Actualizar estado de medicamentos activos a completados
                medicamentos_activos = gestion.medicamentos_asignados.filter(estado='activa')
                # Actualizar fecha_inicio para medicamentos que no la tienen
                medicamentos_sin_inicio = medicamentos_activos.filter(fecha_inicio__isnull=True)
                medicamentos_sin_inicio.update(fecha_inicio=date.today())
                # Actualizar estado y fecha_fin
                medicamentos_activos.update(
                    estado='completada',
                    fecha_fin=date.today()
                )
                
                # Actualizar estado de análisis solicitados a completados
                analisis_solicitados = gestion.analisis_asignados.filter(estado='solicitado')
                # Actualizar fecha_programada para análisis que no la tienen
                analisis_sin_programar = analisis_solicitados.filter(fecha_programada__isnull=True)
                analisis_sin_programar.update(fecha_programada=date.today())
                # Actualizar estado y fecha_completado
                analisis_solicitados.update(
                    estado='completado',
                    fecha_completado=date.today()
                )
                
                messages.success(request, 'Gestión y cita marcadas como completadas. Medicamentos y análisis actualizados.')
                
                base_url = reverse('agenda_doctor')
                return redirect(construir_url_con_filtros(base_url, request))
            
            # Si no es completada, redirigir a la gestión con filtros
            base_url = reverse('gestion:gestionar_cita', kwargs={'cita_id': cita_id})
            return redirect(construir_url_con_filtros(base_url, request))
    else:
        # Para peticiones GET, inicializar el formulario con la instancia
        form = GestionCitaForm(instance=gestion)
    
    # Obtener medicamentos y análisis asignados
    medicamentos_asignados = gestion.medicamentos_asignados.all()
    analisis_asignados = gestion.analisis_asignados.all()
    
    solo_lectura = False
    if cita.estado == 'completada':
        solo_lectura = True
    
    context = {
        'cita': cita,
        'gestion': gestion,
        'form': form,
        'medicamentos_asignados': medicamentos_asignados,
        'analisis_asignados': analisis_asignados,
        'solo_lectura': solo_lectura,
    }
    
    return render(request, 'gestion/gestionar_cita.html', context)

@role_required(['admin', 'doctor'])
def agregar_medicamento(request, gestion_id):
    """
    Vista para agregar un medicamento a una gestión
    """
    gestion = get_object_or_404(GestionCita, pk=gestion_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para modificar esta gestión.')
        return redirect('agenda_doctor')
    
    if request.method == 'POST':
        form = MedicamentoAsignadoForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.gestion = gestion
            medicamento.save()
            messages.success(request, 'Medicamento agregado correctamente.')
            
            base_url = reverse('gestion:gestionar_cita', kwargs={'cita_id': gestion.cita.id})
            return redirect(construir_url_con_filtros(base_url, request))
    else:
        form = MedicamentoAsignadoForm()
    
    context = {
        'gestion': gestion,
        'form': form,
    }
    
    return render(request, 'gestion/agregar_medicamento.html', context)

@role_required(['admin', 'doctor'])
def agregar_analisis(request, gestion_id):
    """
    Vista para agregar un análisis a una gestión
    """
    gestion = get_object_or_404(GestionCita, pk=gestion_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para modificar esta gestión.')
        return redirect('agenda_doctor')
    
    if request.method == 'POST':
        form = AnalisisAsignadoForm(request.POST)
        if form.is_valid():
            analisis = form.save(commit=False)
            analisis.gestion = gestion
            analisis.save()
            messages.success(request, 'Análisis agregado correctamente.')
            
            base_url = reverse('gestion:gestionar_cita', kwargs={'cita_id': gestion.cita.id})
            return redirect(construir_url_con_filtros(base_url, request))
    else:
        form = AnalisisAsignadoForm()
    
    context = {
        'gestion': gestion,
        'form': form,
    }
    
    return render(request, 'gestion/agregar_analisis.html', context)

@role_required(['admin', 'doctor'])
def eliminar_medicamento(request, medicamento_id):
    """
    Vista para eliminar un medicamento asignado
    """
    medicamento = get_object_or_404(MedicamentoAsignado, pk=medicamento_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif medicamento.gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para eliminar este medicamento.')
        return redirect('agenda_doctor')
    
    gestion_id = medicamento.gestion.cita.id
    medicamento.delete()
    messages.success(request, 'Medicamento eliminado correctamente.')
    
    base_url = reverse('gestion:gestionar_cita', kwargs={'cita_id': gestion_id})
    return redirect(construir_url_con_filtros(base_url, request))

@role_required(['admin', 'doctor'])
def eliminar_analisis(request, analisis_id):
    """
    Vista para eliminar un análisis asignado
    """
    analisis = get_object_or_404(AnalisisAsignado, pk=analisis_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif analisis.gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para eliminar este análisis.')
        return redirect('agenda_doctor')
    
    gestion_id = analisis.gestion.cita.id
    analisis.delete()
    messages.success(request, 'Análisis eliminado correctamente.')
    
    base_url = reverse('gestion:gestionar_cita', kwargs={'cita_id': gestion_id})
    return redirect(construir_url_con_filtros(base_url, request))

@role_required(['admin', 'doctor'])
def cambiar_estado_medicamento(request, medicamento_id):
    """
    Vista para cambiar el estado de un medicamento vía AJAX
    """
    if request.method == 'POST':
        medicamento = get_object_or_404(MedicamentoAsignado, pk=medicamento_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in ['activa', 'completada', 'cancelada']:
            medicamento.estado = nuevo_estado
            medicamento.save()
            return JsonResponse({'success': True, 'estado': nuevo_estado})
    
    return JsonResponse({'success': False})

@role_required(['admin', 'doctor'])
def cambiar_estado_analisis(request, analisis_id):
    """
    Vista para cambiar el estado de un análisis vía AJAX
    """
    if request.method == 'POST':
        analisis = get_object_or_404(AnalisisAsignado, pk=analisis_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in ['solicitado', 'en_proceso', 'completado', 'cancelado']:
            analisis.estado = nuevo_estado
            analisis.save()
            return JsonResponse({'success': True, 'estado': nuevo_estado})
    
    return JsonResponse({'success': False})

@role_required(['admin', 'doctor'])
def imprimir_prescripcion(request, gestion_id):
    """
    Vista para imprimir prescripción de medicamentos
    """
    gestion = get_object_or_404(GestionCita, pk=gestion_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para imprimir esta prescripción.')
        return redirect('agenda_doctor')
    
    # Obtener configuración de impresión activa
    config = ConfiguracionImpresion.objects.filter(activo=True).first()
    if not config:
        messages.error(request, 'No hay configuración de impresión activa.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Obtener medicamentos seleccionados
    medicamentos_ids = request.GET.getlist('medicamentos')
    if not medicamentos_ids:
        messages.error(request, 'Debe seleccionar al menos un medicamento.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Verificar límite de elementos
    if len(medicamentos_ids) > config.max_elementos_por_impresion:
        messages.error(request, f'No puede imprimir más de {config.max_elementos_por_impresion} medicamentos por prescripción.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Obtener medicamentos
    medicamentos = MedicamentoAsignado.objects.filter(
        id__in=medicamentos_ids,
        gestion=gestion
    )
    
    if not medicamentos:
        messages.error(request, 'No se encontraron los medicamentos seleccionados.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    context = {
        'gestion': gestion,
        'medicamentos': medicamentos,
        'config': config,
    }
    
    return render(request, 'gestion/imprimir_prescripcion.html', context)

@role_required(['admin', 'doctor'])
def imprimir_analisis(request, gestion_id):
    """
    Vista para imprimir solicitud de análisis
    """
    gestion = get_object_or_404(GestionCita, pk=gestion_id)
    
    # Verificar permisos
    if request.user.role == 'admin':
        pass
    elif gestion.doctor.user != request.user:
        messages.error(request, 'No tienes permisos para imprimir esta solicitud.')
        return redirect('agenda_doctor')
    
    # Obtener configuración de impresión activa
    config = ConfiguracionImpresion.objects.filter(activo=True).first()
    if not config:
        messages.error(request, 'No hay configuración de impresión activa.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Obtener análisis seleccionados
    analisis_ids = request.GET.getlist('analisis')
    if not analisis_ids:
        messages.error(request, 'Debe seleccionar al menos un análisis.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Verificar límite de elementos
    if len(analisis_ids) > config.max_elementos_por_impresion:
        messages.error(request, f'No puede imprimir más de {config.max_elementos_por_impresion} análisis por solicitud.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    # Obtener análisis
    analisis = AnalisisAsignado.objects.filter(
        id__in=analisis_ids,
        gestion=gestion
    )
    
    if not analisis:
        messages.error(request, 'No se encontraron los análisis seleccionados.')
        return redirect('gestion:gestionar_cita', cita_id=gestion.cita.id)
    
    context = {
        'gestion': gestion,
        'analisis': analisis,
        'config': config,
    }
    
    return render(request, 'gestion/imprimir_analisis.html', context)
