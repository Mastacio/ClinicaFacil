from django.contrib import admin
from .models import DoctorPerfil, Especialidad, HorarioDoctor
class HorarioDoctorInline(admin.TabularInline):
    model = HorarioDoctor
    extra = 1
    fields = ('dia_semana', 'hora_inicio', 'hora_fin', 'intervalo_minutos')
    show_change_link = True


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(DoctorPerfil)
class DoctorPerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'identificacion', 'registro_medico', 'activo')
    search_fields = ('user__first_name', 'user__last_name', 'identificacion', 'registro_medico')
    list_filter = ('activo', 'especialidades')
    filter_horizontal = ('especialidades',)
    inlines = [HorarioDoctorInline]

@admin.register(HorarioDoctor)
class HorarioDoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'dia_semana', 'hora_inicio', 'hora_fin', 'intervalo_minutos')
    list_filter = ('doctor', 'dia_semana')
