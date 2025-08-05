from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha', 'doctor')
    search_fields = ('paciente__user__first_name', 'doctor__user__first_name', 'motivo')
