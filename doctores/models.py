
from django.db import models
from users.models import User


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


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
    dia_semana = models.IntegerField(choices=[(i, d) for i, d in enumerate(['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'])])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    intervalo_minutos = models.PositiveIntegerField(default=30, help_text="Duración de cada cita en minutos para este día/horario")

    class Meta:
        unique_together = ('doctor', 'dia_semana', 'hora_inicio', 'hora_fin')
        ordering = ['doctor', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f"{self.get_dia_semana_display()} {self.hora_inicio} - {self.hora_fin} ({self.intervalo_minutos} min)"
