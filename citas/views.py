
from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cita
from .forms import CitaForm
from pacientes.models import PacientePerfil
from doctores.models import DoctorPerfil
from users.models import User
from django.template.loader import render_to_string
from users.decorators import (
    role_required, admin_required, doctor_required, 
    asistente_required, paciente_required, staff_required,
    cita_owner_required
)

# API para búsqueda de pacientes (select2)
@staff_required
def api_buscar_pacientes(request):
    q = request.GET.get('q', '')
    pacientes = PacientePerfil.objects.filter(user__first_name__icontains=q)[:10]
    results = [
        {'id': p.id, 'text': f"{p.user.get_full_name()} ({p.user.email})"}
        for p in pacientes
    ]
    return JsonResponse({'results': results, 'has_next': False})

# API para búsqueda de doctores (select2)
@staff_required
def api_buscar_doctores(request):
    q = request.GET.get('q', '')
    doctores = DoctorPerfil.objects.filter(user__first_name__icontains=q)[:10]
    results = [
        {'id': d.id, 'text': f"{d.user.get_full_name()} ({d.user.email})"}
        for d in doctores
    ]
    return JsonResponse({'results': results, 'has_next': False})

@doctor_required
def calendario_doctor(request):
    # Obtener todos los doctores activos
    doctores = DoctorPerfil.objects.filter(activo=True)
    doctor_id = request.GET.get('doctor')
    doctor = None
    if doctor_id:
        doctor = DoctorPerfil.objects.filter(id=doctor_id).first()
    if not doctor and doctores.exists():
        doctor = doctores.first()
    
    # Obtener horarios del doctor
    horarios = doctor.horarios.all() if doctor else []
    
    # Días de la semana
    dias_semana = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    dias_idx = list(range(7))
    
    # Construir intervalos de tiempo según el horario y el intervalo definido por día
    intervalos_set = set()
    intervalos_horarios = {}
    for h in horarios:
        t = h.hora_inicio
        while t < h.hora_fin:
            intervalo = t.strftime('%H:%M')
            intervalos_set.add(intervalo)
            if intervalo not in intervalos_horarios:
                intervalos_horarios[intervalo] = {}
            intervalos_horarios[intervalo][h.dia_semana] = True
            # Avanzar según el intervalo definido para ese horario
            t = (datetime.combine(datetime.today(), t) + timedelta(minutes=h.intervalo_minutos)).time()
    intervalos = sorted(list(intervalos_set))
    
    # Mapear citas existentes con información detallada por fecha real
    citas_detalladas = {}
    if doctor:
        # Obtener citas del mes actual y el siguiente para mostrar en el calendario
        hoy = datetime.today().date()
        inicio_mes = hoy.replace(day=1)
        fin_mes = (inicio_mes.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        print(f"DEBUG: Buscando citas para doctor {doctor.id} desde {inicio_mes} hasta {fin_mes}")
        
        citas = Cita.objects.filter(
            doctor=doctor, 
            fecha__gte=inicio_mes,
            fecha__lte=fin_mes
        ).select_related('paciente')
        
        print(f"DEBUG: Encontradas {citas.count()} citas")
        
        for cita in citas:
            fecha_str = cita.fecha.strftime('%Y-%m-%d')
            hora_inicio = cita.hora_inicio.strftime('%H:%M')
            hora_fin = cita.hora_fin.strftime('%H:%M')
            
            print(f"DEBUG: Procesando cita - Fecha: {fecha_str}, Hora: {hora_inicio}-{hora_fin}, Paciente: {cita.paciente}")
            
            if fecha_str not in citas_detalladas:
                citas_detalladas[fecha_str] = {}
            
            citas_detalladas[fecha_str][hora_inicio] = {
                'paciente': str(cita.paciente),
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'fecha': str(cita.fecha),
                'estado': cita.estado,
                'motivo': cita.motivo
            }
    
    print(f"DEBUG: Citas detalladas: {citas_detalladas}")
    
    # Construir slots detallados por fecha específica
    slots_detallados = {}
    
    # Generar slots para el mes actual
    hoy = datetime.today().date()
    inicio_mes = hoy.replace(day=1)
    fin_mes = (inicio_mes.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    
    print(f"DEBUG: Generando slots desde {inicio_mes} hasta {fin_mes}")
    print(f"DEBUG: Horarios disponibles: {[f'{h.dia_semana}: {h.hora_inicio}-{h.hora_fin}' for h in horarios]}")
    
    fecha_actual = inicio_mes
    while fecha_actual <= fin_mes:
        fecha_str = fecha_actual.strftime('%Y-%m-%d')
        dia_semana = fecha_actual.weekday()  # 0=Lunes, 1=Martes, etc.
        
        # Buscar horarios para este día de la semana
        horarios_dia = [h for h in horarios if h.dia_semana == dia_semana]
        
        if horarios_dia:
            slots_detallados[fecha_str] = {}
            print(f"DEBUG: Generando slots para {fecha_str} (día {dia_semana})")
            
            for horario in horarios_dia:
                t = horario.hora_inicio
                while t < horario.hora_fin:
                    intervalo = t.strftime('%H:%M')
                    
                    # Calcular hora fin del slot
                    hora_fin_slot = (datetime.combine(datetime.today(), t) + 
                                   timedelta(minutes=horario.intervalo_minutos)).time()
                    hora_fin_str = hora_fin_slot.strftime('%H:%M')
                    
                    # Verificar si el slot está ocupado
                    esta_ocupado = False
                    info_cita = None
                    if fecha_str in citas_detalladas and intervalo in citas_detalladas[fecha_str]:
                        esta_ocupado = True
                        info_cita = citas_detalladas[fecha_str][intervalo]
                    
                    # Guardar información detallada del slot
                    slots_detallados[fecha_str][intervalo] = {
                        'hora_inicio': intervalo,
                        'hora_fin': hora_fin_str,
                        'esta_ocupado': esta_ocupado,
                        'info_cita': info_cita,
                        'intervalo_minutos': horario.intervalo_minutos
                    }
                    
                    t = hora_fin_slot
        
        fecha_actual += timedelta(days=1)
    
    print(f"DEBUG: Slots detallados generados: {len(slots_detallados)} fechas")
    for fecha, slots in list(slots_detallados.items())[:3]:  # Mostrar solo las primeras 3 fechas
        print(f"DEBUG: {fecha}: {len(slots)} slots")
    
    # Construir intervalos_por_dia para compatibilidad (mantener estructura anterior)
    intervalos_por_dia = {i: [] for i in dias_idx}
    for h in horarios:
        t = h.hora_inicio
        while t < h.hora_fin:
            intervalo = t.strftime('%H:%M')
            if intervalo not in intervalos_por_dia[h.dia_semana]:
                intervalos_por_dia[h.dia_semana].append(intervalo)
            t = (datetime.combine(datetime.today(), t) + timedelta(minutes=h.intervalo_minutos)).time()
    
    # Ordenar los intervalos de cada día
    for k in intervalos_por_dia:
        intervalos_por_dia[k].sort()
    
    import json
    context = {
        'doctores': doctores,
        'doctor': doctor,
        'dias_semana': dias_semana,
        'dias_idx': dias_idx,
        'intervalos': intervalos,
        'intervalos_horarios': intervalos_horarios,
        'citas_map_json': json.dumps(citas_detalladas),
        'horarios_doctor': {h.dia_semana: h for h in horarios},
        'semana_actual': [],  # Ya no se usa, se calcula por fecha
        'fecha_actual': hoy,
        'intervalos_por_dia': json.dumps(intervalos_por_dia),
        'slots_detallados': json.dumps(slots_detallados),
    }
    return render(request, 'citas/calendario_doctor.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cita
from .forms import CitaForm
from pacientes.models import PacientePerfil
from doctores.models import DoctorPerfil
from users.models import User

@staff_required
def gestionar_citas(request):
    # Filtrar por rol
    if request.user.role == 'doctor':
        citas = Cita.objects.filter(doctor__user=request.user)
    elif request.user.role == 'paciente':
        citas = Cita.objects.filter(paciente__user=request.user)
    else:
        citas = Cita.objects.all()
    citas = citas.order_by('-fecha', 'hora_inicio')
    
    # Calcular estadísticas
    total_citas = citas.count()
    citas_pendientes = citas.filter(estado='pendiente').count()
    citas_confirmadas = citas.filter(estado='confirmada').count()
    citas_completadas = citas.filter(estado='completada').count()
    citas_canceladas = citas.filter(estado='cancelada').count()
    
    context = {
        'citas': citas,
        'total_citas': total_citas,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
    }
    
    return render(request, 'citas/gestionar_citas.html', context)

@staff_required
def crear_cita(request):
    doctor_id = request.GET.get('doctor')
    paciente_id = request.GET.get('paciente')
    initial = {}
    if doctor_id:
        initial['doctor'] = doctor_id
    if paciente_id:
        initial['paciente'] = paciente_id
    fecha = request.GET.get('fecha')
    hora_inicio = request.GET.get('hora_inicio')
    if fecha:
        initial['fecha'] = fecha
    if hora_inicio:
        initial['hora_inicio'] = hora_inicio
    if request.method == 'POST':
        form = CitaForm(request.POST, initial=initial)
        if form.is_valid():
            cita = form.save(commit=False)
            # Si el campo paciente está oculto, asignar manualmente
            if paciente_id:
                cita.paciente = PacientePerfil.objects.get(pk=paciente_id)
            if doctor_id:
                cita.doctor = DoctorPerfil.objects.get(pk=doctor_id)
            cita.creada_por = request.user
            cita.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Cita creada correctamente.')
            return redirect('gestionar_citas')
    else:
        form = CitaForm(initial=initial)
    ocultar_doctor = bool(doctor_id)
    ocultar_paciente = bool(paciente_id)
    
    return render(request, 'citas/crear_cita.html', {
        'form': form, 
        'ocultar_doctor': ocultar_doctor, 
        'ocultar_paciente': ocultar_paciente
    })

@staff_required
def crear_cita_modal(request):
    """
    Vista específica para el formulario del modal de creación de citas
    """
    doctor_id = request.GET.get('doctor')
    paciente_id = request.GET.get('paciente')
    initial = {}
    
    # Configurar valores iniciales
    if doctor_id:
        initial['doctor'] = doctor_id
    if paciente_id:
        initial['paciente'] = paciente_id
    
    fecha = request.GET.get('fecha')
    hora_inicio = request.GET.get('hora_inicio')
    if fecha:
        initial['fecha'] = fecha
    if hora_inicio:
        initial['hora_inicio'] = hora_inicio
        
        # Calcular hora fin automáticamente
        if doctor_id and hora_inicio:
            try:
                from datetime import datetime, timedelta
                from doctores.models import HorarioDoctor
                
                # Obtener el doctor
                doctor = DoctorPerfil.objects.get(pk=doctor_id)
                
                # Convertir fecha a objeto datetime para obtener el día de la semana
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                dia_semana = fecha_obj.weekday()  # 0=Lunes, 1=Martes, etc.
                
                # Buscar el horario del doctor para ese día
                horario = HorarioDoctor.objects.filter(
                    doctor=doctor,
                    dia_semana=dia_semana
                ).first()
                
                if horario:
                    # Calcular hora fin basándose en el intervalo
                    hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
                    hora_fin_obj = (datetime.combine(datetime.today(), hora_inicio_obj) + 
                                  timedelta(minutes=horario.intervalo_minutos)).time()
                    initial['hora_fin'] = hora_fin_obj.strftime('%H:%M')
                    
                    print(f"Hora inicio: {hora_inicio}, Intervalo: {horario.intervalo_minutos} min, Hora fin: {initial['hora_fin']}")
                
            except Exception as e:
                print(f"Error calculando hora fin: {e}")
                # Si hay error, usar intervalo por defecto de 30 minutos
                try:
                    hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
                    hora_fin_obj = (datetime.combine(datetime.today(), hora_inicio_obj) + 
                                  timedelta(minutes=30)).time()
                    initial['hora_fin'] = hora_fin_obj.strftime('%H:%M')
                except:
                    pass
    
    # Manejar POST del formulario del modal
    if request.method == 'POST':
        form = CitaForm(request.POST, initial=initial)
        if form.is_valid():
            cita = form.save(commit=False)
            # Si el campo paciente está oculto, asignar manualmente
            if paciente_id:
                cita.paciente = PacientePerfil.objects.get(pk=paciente_id)
            if doctor_id:
                cita.doctor = DoctorPerfil.objects.get(pk=doctor_id)
            cita.creada_por = request.user
            cita.save()
            
            # Verificar si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Retornar respuesta JSON para el modal
                return JsonResponse({
                    'success': True,
                    'message': 'Cita creada correctamente.',
                    'cita_id': cita.id
                })
            else:
                # Petición normal, redirigir
                messages.success(request, 'Cita creada correctamente.')
                return redirect('gestionar_citas')
        else:
            # Si hay errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Retornar JSON con errores para AJAX
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                    'html': render_to_string('citas/_form_cita_modal.html', {
                        'form': form,
                        'ocultar_doctor': bool(doctor_id),
                        'ocultar_paciente': bool(paciente_id)
                    }, request=request)
                })
            else:
                # Petición normal, mostrar formulario con errores
                return render(request, 'citas/_form_cita_modal.html', {
                    'form': form,
                    'ocultar_doctor': bool(doctor_id),
                    'ocultar_paciente': bool(paciente_id)
                })
    else:
        form = CitaForm(initial=initial)
    
    # Variables para el template
    ocultar_doctor = bool(doctor_id)
    ocultar_paciente = bool(paciente_id)
    
    return render(request, 'citas/_form_cita_modal.html', {
        'form': form,
        'ocultar_doctor': ocultar_doctor,
        'ocultar_paciente': ocultar_paciente
    })

@cita_owner_required
def ver_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    return render(request, 'citas/ver_cita.html', {'cita': cita})

@staff_required
def cancelar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if cita.estado == 'pendiente':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada.')
    return redirect('gestionar_citas')

@doctor_required
def agenda_doctor(request):
    """
    Vista para la agenda de citas del doctor
    """
    print(f"DEBUG: Usuario: {request.user.username}, Rol: {request.user.role}")
    
    # Obtener parámetros de filtro
    fecha_filtro = request.GET.get('fecha')
    estado_filtro = request.GET.get('estado')
    paciente_filtro = request.GET.get('paciente')
    doctor_filtro = request.GET.get('doctor')
    
    print(f"DEBUG: Filtros - fecha: {fecha_filtro}, estado: {estado_filtro}, paciente: {paciente_filtro}, doctor: {doctor_filtro}")
    
    # Determinar qué doctor mostrar
    doctor = None
    es_admin = request.user.role == 'admin'
    
    if es_admin:
        # Admin puede ver agenda de cualquier doctor
        if doctor_filtro:
            doctor = DoctorPerfil.objects.filter(id=doctor_filtro, activo=True).first()
            print(f"DEBUG: Admin seleccionó doctor ID {doctor_filtro}, encontrado: {doctor}")
            if not doctor:
                messages.error(request, 'Doctor no encontrado.')
                return redirect('agenda_doctor')
        else:
            # Si no seleccionó doctor, usar el primero disponible
            doctor = DoctorPerfil.objects.filter(activo=True).first()
            print(f"DEBUG: Admin sin selección, usando primer doctor: {doctor}")
            if not doctor:
                messages.error(request, 'No hay doctores disponibles.')
                return redirect('gestionar_citas')
    else:
        # Doctor ve solo su propia agenda
        doctor = DoctorPerfil.objects.filter(user=request.user, activo=True).first()
        print(f"DEBUG: Buscando doctor para usuario {request.user.username}, encontrado: {doctor}")
        if not doctor:
            messages.error(request, 'No tienes un perfil de doctor configurado.')
            return redirect('gestionar_citas')
    
    # Obtener todos los doctores para el filtro (solo para admin)
    doctores_disponibles = []
    if es_admin:
        doctores_disponibles = DoctorPerfil.objects.filter(activo=True).select_related('user')
        print(f"DEBUG: Doctores disponibles para admin: {doctores_disponibles.count()}")
    
    # Filtrar citas del doctor
    citas = Cita.objects.filter(doctor=doctor).select_related('paciente__user')
    print(f"DEBUG: Citas encontradas para doctor {doctor}: {citas.count()}")
    
    # Aplicar filtros
    if fecha_filtro:
        try:
            fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            citas = citas.filter(fecha=fecha_obj)
            print(f"DEBUG: Filtro por fecha {fecha_obj}, citas restantes: {citas.count()}")
        except ValueError:
            print(f"DEBUG: Error al parsear fecha {fecha_filtro}")
            pass
    else:
        # Por defecto, mostrar citas del día actual
        citas = citas.filter(fecha=datetime.today().date())
        print(f"DEBUG: Mostrando citas del día actual, encontradas: {citas.count()}")
    
    if estado_filtro:
        citas = citas.filter(estado=estado_filtro)
        print(f"DEBUG: Filtro por estado {estado_filtro}, citas restantes: {citas.count()}")
    
    if paciente_filtro:
        citas = citas.filter(paciente__user__first_name__icontains=paciente_filtro) | \
                citas.filter(paciente__user__last_name__icontains=paciente_filtro)
        print(f"DEBUG: Filtro por paciente {paciente_filtro}, citas restantes: {citas.count()}")
    
    # Ordenar por fecha y hora
    citas = citas.order_by('fecha', 'hora_inicio')
    
    # Estadísticas
    total_citas = citas.count()
    citas_pendientes = citas.filter(estado='pendiente').count()
    citas_confirmadas = citas.filter(estado='confirmada').count()
    citas_completadas = citas.filter(estado='completada').count()
    citas_canceladas = citas.filter(estado='cancelada').count()
    
    print(f"DEBUG: Estadísticas - Total: {total_citas}, Pendientes: {citas_pendientes}, Confirmadas: {citas_confirmadas}")
    
    context = {
        'citas': citas,
        'doctor': doctor,
        'fecha_filtro': fecha_filtro or datetime.today().strftime('%Y-%m-%d'),
        'estado_filtro': estado_filtro,
        'paciente_filtro': paciente_filtro,
        'doctor_filtro': doctor_filtro,
        'doctores_disponibles': doctores_disponibles,
        'total_citas': total_citas,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
        'estados_choices': Cita.ESTADO_CHOICES,
        'es_admin': es_admin,
    }
    
    print(f"DEBUG: Contexto preparado, renderizando template")
    return render(request, 'citas/agenda_doctor.html', context)

@doctor_required
def cancelar_cita_agenda(request, pk):
    """
    Vista para cancelar cita desde la agenda
    """
    from django.urls import reverse
    
    cita = get_object_or_404(Cita, pk=pk)
    
    # Verificar permisos
    if request.user.role == 'admin':
        # Admin puede cancelar citas de cualquier doctor
        pass
    elif cita.doctor.user != request.user:
        # Doctor solo puede cancelar sus propias citas
        messages.error(request, 'No tienes permisos para cancelar esta cita.')
        return redirect('agenda_doctor')
    
    if cita.estado == 'pendiente':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada correctamente.')
    else:
        messages.warning(request, 'Solo se pueden cancelar citas pendientes.')
    
    # Construir URL de retorno con filtros actuales
    params = []
    
    # Agregar filtros actuales
    if request.GET.get('fecha'):
        params.append(f"fecha={request.GET.get('fecha')}")
    if request.GET.get('estado'):
        params.append(f"estado={request.GET.get('estado')}")
    if request.GET.get('paciente'):
        params.append(f"paciente={request.GET.get('paciente')}")
    if request.GET.get('doctor'):
        params.append(f"doctor={request.GET.get('doctor')}")
    
    # Construir la URL completa
    base_url = reverse('agenda_doctor')
    if params:
        base_url += '?' + '&'.join(params)
    
    return redirect(base_url)

@doctor_required
def confirmar_cita_agenda(request, pk):
    """
    Vista para confirmar cita desde la agenda
    """
    from django.urls import reverse
    
    cita = get_object_or_404(Cita, pk=pk)
    
    # Verificar permisos
    if request.user.role == 'admin':
        # Admin puede confirmar citas de cualquier doctor
        pass
    elif cita.doctor.user != request.user:
        # Doctor solo puede confirmar sus propias citas
        messages.error(request, 'No tienes permisos para confirmar esta cita.')
        return redirect('agenda_doctor')
    
    if cita.estado == 'pendiente':
        cita.estado = 'confirmada'
        cita.save()
        messages.success(request, 'Cita confirmada correctamente.')
    else:
        messages.warning(request, 'Solo se pueden confirmar citas pendientes.')
    
    # Construir URL de retorno con filtros actuales
    params = []
    
    # Agregar filtros actuales
    if request.GET.get('fecha'):
        params.append(f"fecha={request.GET.get('fecha')}")
    if request.GET.get('estado'):
        params.append(f"estado={request.GET.get('estado')}")
    if request.GET.get('paciente'):
        params.append(f"paciente={request.GET.get('paciente')}")
    if request.GET.get('doctor'):
        params.append(f"doctor={request.GET.get('doctor')}")
    
    # Construir la URL completa
    base_url = reverse('agenda_doctor')
    if params:
        base_url += '?' + '&'.join(params)
    
    return redirect(base_url)

@staff_required
def confirmar_cita(request, pk):
    """
    Vista para confirmar cita desde la gestión general
    """
    cita = get_object_or_404(Cita, pk=pk)
    
    if cita.estado == 'pendiente':
        cita.estado = 'confirmada'
        cita.save()
        messages.success(request, 'Cita confirmada correctamente.')
    else:
        messages.warning(request, 'Solo se pueden confirmar citas pendientes.')
    
    return redirect('gestionar_citas')

@paciente_required
def mis_citas(request):
    """
    Vista para que los pacientes vean, creen y cancelen sus citas
    """
    # Verificar que el usuario sea paciente
    if request.user.role != 'paciente':
        messages.error(request, 'Acceso denegado. Solo los pacientes pueden acceder a esta sección.')
        return redirect('welcome')
    
    # Obtener el perfil del paciente
    try:
        paciente = PacientePerfil.objects.get(user=request.user)
    except PacientePerfil.DoesNotExist:
        messages.error(request, 'No tienes un perfil de paciente configurado.')
        return redirect('welcome')
    
    # Obtener citas del paciente
    citas = Cita.objects.filter(paciente=paciente).select_related('doctor__user').order_by('-fecha', 'hora_inicio')
    
    # Aplicar filtros
    estado_filtro = request.GET.get('estado')
    fecha_filtro = request.GET.get('fecha')
    
    if estado_filtro:
        citas = citas.filter(estado=estado_filtro)
    
    if fecha_filtro:
        try:
            fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            citas = citas.filter(fecha=fecha_obj)
        except ValueError:
            pass
    
    # Estadísticas
    total_citas = citas.count()
    citas_pendientes = citas.filter(estado='pendiente').count()
    citas_confirmadas = citas.filter(estado='confirmada').count()
    citas_completadas = citas.filter(estado='completada').count()
    citas_canceladas = citas.filter(estado='cancelada').count()
    
    # Obtener doctores disponibles para crear nuevas citas
    doctores_disponibles = DoctorPerfil.objects.filter(activo=True).select_related('user')
    
    context = {
        'citas': citas,
        'paciente': paciente,
        'estado_filtro': estado_filtro,
        'fecha_filtro': fecha_filtro,
        'total_citas': total_citas,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
        'estados_choices': Cita.ESTADO_CHOICES,
        'doctores_disponibles': doctores_disponibles,
    }
    
    return render(request, 'citas/mis_citas.html', context)

@paciente_required
def crear_cita_paciente(request):
    """
    Vista para que los pacientes creen sus propias citas
    """
    # Verificar que el usuario sea paciente
    if request.user.role != 'paciente':
        messages.error(request, 'Acceso denegado. Solo los pacientes pueden acceder a esta sección.')
        return redirect('welcome')
    
    # Obtener el perfil del paciente
    try:
        paciente = PacientePerfil.objects.get(user=request.user)
    except PacientePerfil.DoesNotExist:
        messages.error(request, 'No tienes un perfil de paciente configurado.')
        return redirect('welcome')
    
    doctor_id = request.GET.get('doctor')
    fecha = request.GET.get('fecha')
    hora_inicio = request.GET.get('hora_inicio')
    
    initial = {}
    if doctor_id:
        initial['doctor'] = doctor_id
    if fecha:
        initial['fecha'] = fecha
    if hora_inicio:
        initial['hora_inicio'] = hora_inicio
    
    if request.method == 'POST':
        form = CitaForm(request.POST, initial=initial)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = paciente
            cita.creada_por = request.user
            cita.save()
            messages.success(request, 'Cita creada correctamente.')
            return redirect('mis_citas')
    else:
        form = CitaForm(initial=initial)
    
    # Obtener doctores disponibles
    doctores_disponibles = DoctorPerfil.objects.filter(activo=True).select_related('user')
    
    return render(request, 'citas/crear_cita_paciente.html', {
        'form': form,
        'doctores_disponibles': doctores_disponibles,
        'paciente': paciente
    })

@paciente_required
def cancelar_cita_paciente(request, pk):
    """
    Vista para que los pacientes cancelen sus citas
    """
    cita = get_object_or_404(Cita, pk=pk)
    
    # Verificar que la cita pertenezca al paciente
    if cita.paciente.user != request.user:
        messages.error(request, 'No tienes permisos para cancelar esta cita.')
        return redirect('mis_citas')
    
    if cita.estado == 'pendiente':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada correctamente.')
    else:
        messages.warning(request, 'Solo se pueden cancelar citas pendientes.')
    
    return redirect('mis_citas')

@paciente_required
def confirmar_cita_paciente(request, pk):
    """
    Vista para que los pacientes confirmen sus citas (opcional)
    """
    cita = get_object_or_404(Cita, pk=pk)
    
    # Verificar que la cita pertenezca al paciente
    if cita.paciente.user != request.user:
        messages.error(request, 'No tienes permisos para confirmar esta cita.')
        return redirect('mis_citas')
    
    if cita.estado == 'pendiente':
        cita.estado = 'confirmada'
        cita.save()
        messages.success(request, 'Cita confirmada correctamente.')
    else:
        messages.warning(request, 'Solo se pueden confirmar citas pendientes.')
    
    return redirect('mis_citas')
