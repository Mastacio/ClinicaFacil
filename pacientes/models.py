from django.db import models
from django.conf import settings

class PacientePerfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_paciente')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=[('masculino','Masculino'),('femenino','Femenino'),('otro','Otro')], blank=True)
    tipo_sangre = models.CharField(max_length=3, choices=[('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')], blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, blank=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True)
    alergias = models.TextField(blank=True)
    enfermedades_cronicas = models.TextField(blank=True)
    medicamentos = models.TextField(blank=True)
    antecedentes_quirurgicos = models.TextField(blank=True)
    antecedentes_familiares = models.TextField(blank=True)
    seguro_medico = models.CharField(max_length=100, blank=True)
    numero_seguro = models.CharField(max_length=100, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True)
    estado_civil = models.CharField(max_length=20, blank=True)
    notas = models.TextField(blank=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
