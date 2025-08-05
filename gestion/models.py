from django.db import models
from citas.models import Cita
from pacientes.models import PacientePerfil
from doctores.models import DoctorPerfil

class Medicamento(models.Model):
    """
    Modelo para medicamentos disponibles
    """
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    presentacion = models.CharField(max_length=100, blank=True)
    dosis_recomendada = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Analisis(models.Model):
    """
    Modelo para análisis médicos disponibles
    """
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=100, blank=True)
    preparacion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Análisis'

    def __str__(self):
        return self.nombre

class GestionCita(models.Model):
    """
    Modelo para la gestión de una cita médica
    """
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='gestion')
    paciente = models.ForeignKey(PacientePerfil, on_delete=models.CASCADE, related_name='gestiones')
    doctor = models.ForeignKey(DoctorPerfil, on_delete=models.CASCADE, related_name='gestiones')
    
    # Información de la consulta
    motivo_consulta = models.TextField(blank=True)
    sintomas = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    
    # Estado de la gestión
    ESTADO_CHOICES = [
        ('iniciada', 'Iniciada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='iniciada')
    
    # Fechas
    fecha_consulta = models.DateField(auto_now_add=True)
    proxima_cita = models.DateField(null=True, blank=True)
    
    # Usuario que creó la gestión
    creado_por = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='gestiones_creadas')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_consulta', '-creado_en']

    def __str__(self):
        return f"Gestión de {self.paciente} - {self.fecha_consulta}"

class MedicamentoAsignado(models.Model):
    """
    Modelo para medicamentos asignados en una gestión
    """
    gestion = models.ForeignKey(GestionCita, on_delete=models.CASCADE, related_name='medicamentos_asignados')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='asignaciones')
    
    # Detalles de la prescripción
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    instrucciones = models.TextField(blank=True)
    
    # Estado de la prescripción
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    
    # Fechas
    fecha_prescripcion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_prescripcion']

    def __str__(self):
        return f"{self.medicamento} - {self.gestion.paciente}"

class AnalisisAsignado(models.Model):
    """
    Modelo para análisis asignados en una gestión
    """
    gestion = models.ForeignKey(GestionCita, on_delete=models.CASCADE, related_name='analisis_asignados')
    analisis = models.ForeignKey(Analisis, on_delete=models.CASCADE, related_name='asignaciones')
    
    # Detalles del análisis
    instrucciones = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    
    # Estado del análisis
    ESTADO_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='solicitado')
    
    # Fechas
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_programada = models.DateField(null=True, blank=True)
    fecha_completado = models.DateField(null=True, blank=True)
    
    # Resultados
    resultado = models.TextField(blank=True)
    archivo_resultado = models.FileField(upload_to='analisis_resultados/', null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name_plural = 'Análisis Asignados'

    def __str__(self):
        return f"{self.analisis} - {self.gestion.paciente}"

class ConfiguracionImpresion(models.Model):
    """
    Modelo para configuración de impresión de prescripciones y análisis
    """
    nombre = models.CharField(max_length=100, default='Configuración Principal')
    activo = models.BooleanField(default=True)
    
    # Archivos de timbrado
    archivo_timbrado = models.FileField(
        upload_to='configuracion_impresion/timbrado/',
        help_text='Archivo PNG del timbrado oficial'
    )
    
    # Firma del doctor
    firma_doctor = models.ImageField(
        upload_to='configuracion_impresion/firmas/',
        help_text='Imagen PNG de la firma del doctor'
    )
    
    # Sello de la clínica
    sello_clinica = models.ImageField(
        upload_to='configuracion_impresion/sellos/',
        help_text='Imagen PNG del sello de la clínica'
    )
    
    # Configuración de impresión
    max_elementos_por_impresion = models.PositiveIntegerField(
        default=3,
        help_text='Máximo número de elementos por impresión'
    )
    
    # Información de la clínica para impresión
    nombre_clinica = models.CharField(max_length=200, blank=True)
    direccion_clinica = models.TextField(blank=True)
    telefono_clinica = models.CharField(max_length=50, blank=True)
    email_clinica = models.EmailField(blank=True)
    
    # Configuración de página
    margen_superior = models.PositiveIntegerField(default=20, help_text='Margen superior en mm')
    margen_inferior = models.PositiveIntegerField(default=20, help_text='Margen inferior en mm')
    margen_izquierdo = models.PositiveIntegerField(default=20, help_text='Margen izquierdo en mm')
    margen_derecho = models.PositiveIntegerField(default=20, help_text='Margen derecho en mm')
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración de Impresión'
        verbose_name_plural = 'Configuraciones de Impresión'
        ordering = ['-activo', '-creado_en']

    def __str__(self):
        return f"{self.nombre} - {'Activo' if self.activo else 'Inactivo'}"

    def save(self, *args, **kwargs):
        # Si este registro se marca como activo, desactivar los demás
        if self.activo:
            ConfiguracionImpresion.objects.exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)
