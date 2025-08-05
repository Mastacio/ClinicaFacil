
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('paciente', 'Paciente'),
        ('doctor', 'Doctor'),
        ('asistente', 'Asistente'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='paciente')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        # Si el usuario es superuser, asignar rol admin
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
