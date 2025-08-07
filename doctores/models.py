
from django.db import models
from users.models import User


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Consultorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=255, blank=True)
    capacidad = models.PositiveIntegerField(default=1, help_text="Número máximo de pacientes que puede atender simultáneamente")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_doctores_activos(self):
        """Retorna los doctores que usan este consultorio en horarios activos"""
        return DoctorPerfil.objects.filter(
            horarios__consultorio=self,
            activo=True
        ).distinct()

    def get_horarios_activos(self):
        """Retorna los horarios activos de este consultorio"""
        return self.horarios.filter(doctor__activo=True).order_by('doctor', 'dia_semana', 'hora_inicio')


class DoctorPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_doctor')
    identificacion = models.CharField(max_length=30, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    especialidades = models.ManyToManyField(Especialidad, related_name='doctores')
    registro_medico = models.CharField(max_length=50, blank=True)
    universidad = models.CharField(max_length=100, blank=True)
    anios_experiencia = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class HorarioDoctor(models.Model):
    doctor = models.ForeignKey(DoctorPerfil, on_delete=models.CASCADE, related_name='horarios')
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, related_name='horarios', null=True, blank=True)
    dia_semana = models.IntegerField(choices=[(i, d) for i, d in enumerate(['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    intervalo_minutos = models.PositiveIntegerField(default=30, help_text="Duración de cada cita en minutos para este día/horario")

    class Meta:
        unique_together = ('doctor', 'consultorio', 'dia_semana', 'hora_inicio', 'hora_fin')
        ordering = ['doctor', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f"{self.doctor} - {self.consultorio} - {self.get_dia_semana_display()} {self.hora_inicio} - {self.hora_fin}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.db.models import Q
        
        # Validar que el horario no se solape con otros horarios del mismo consultorio
        if self.consultorio:  # Solo validar si hay consultorio asignado
            if self.pk:  # Si es una actualización
                horarios_conflictivos = HorarioDoctor.objects.filter(
                    consultorio=self.consultorio,
                    dia_semana=self.dia_semana,
                    pk__ne=self.pk
                ).filter(
                    Q(hora_inicio__lt=self.hora_fin, hora_fin__gt=self.hora_inicio)
                )
            else:  # Si es una creación
                horarios_conflictivos = HorarioDoctor.objects.filter(
                    consultorio=self.consultorio,
                    dia_semana=self.dia_semana
                ).filter(
                    Q(hora_inicio__lt=self.hora_fin, hora_fin__gt=self.hora_inicio)
                )
            
            if horarios_conflictivos.exists():
                conflictos = []
                for horario in horarios_conflictivos:
                    conflictos.append(f"{horario.doctor} ({horario.get_dia_semana_display()} {horario.hora_inicio}-{horario.hora_fin})")
                
                raise ValidationError(
                    f'El consultorio {self.consultorio} ya está ocupado en este horario por: {", ".join(conflictos)}'
                )
