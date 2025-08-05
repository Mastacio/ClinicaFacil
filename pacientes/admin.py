from django.contrib import admin
from .models import PacientePerfil

@admin.register(PacientePerfil)
class PacientePerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_nacimiento', 'telefono', 'completado')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telefono')
    list_filter = ('completado', 'sexo', 'tipo_sangre')
