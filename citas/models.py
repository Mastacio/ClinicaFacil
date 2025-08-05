from django.db import models
from users.models import User
from doctores.models import DoctorPerfil
from pacientes.models import PacientePerfil

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    paciente = models.ForeignKey(PacientePerfil, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(DoctorPerfil, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=255)
    notas = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_creadas')
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'fecha', 'hora_inicio', 'hora_fin')
        ordering = ['-fecha', 'hora_inicio']

    def __str__(self):
        return f"Cita de {self.paciente} con {self.doctor} el {self.fecha} a las {self.hora_inicio}"
