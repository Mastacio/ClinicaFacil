from django.db import models


class ClinicInfo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    mision = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    valores = models.TextField(blank=True, null=True)
    nosotros = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    horario = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
