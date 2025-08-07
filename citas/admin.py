from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'consultorio', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha', 'doctor', 'consultorio')
    search_fields = ('paciente__user__first_name', 'doctor__user__first_name', 'consultorio__nombre', 'motivo')
    list_select_related = ('paciente__user', 'doctor__user', 'consultorio')
