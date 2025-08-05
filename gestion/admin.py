from django.contrib import admin
from .models import Medicamento, Analisis, GestionCita, MedicamentoAsignado, AnalisisAsignado, ConfiguracionImpresion

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'presentacion', 'dosis_recomendada', 'activo', 'creado_en']
    list_filter = ['activo', 'creado_en']
    search_fields = ['nombre', 'descripcion', 'presentacion']
    list_editable = ['activo']
    ordering = ['nombre']

@admin.register(Analisis)
class AnalisisAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'activo', 'creado_en']
    list_filter = ['activo', 'tipo', 'creado_en']
    search_fields = ['nombre', 'descripcion', 'tipo']
    list_editable = ['activo']
    ordering = ['nombre']

class MedicamentoAsignadoInline(admin.TabularInline):
    model = MedicamentoAsignado
    extra = 1
    fields = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'estado', 'fecha_inicio', 'fecha_fin']

class AnalisisAsignadoInline(admin.TabularInline):
    model = AnalisisAsignado
    extra = 1
    fields = ['analisis', 'estado', 'fecha_programada', 'instrucciones']

@admin.register(GestionCita)
class GestionCitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'doctor', 'estado', 'fecha_consulta', 'proxima_cita']
    list_filter = ['estado', 'fecha_consulta', 'doctor', 'creado_en']
    search_fields = ['paciente__user__first_name', 'paciente__user__last_name', 'doctor__user__first_name']
    readonly_fields = ['creado_en', 'actualizado_en']
    inlines = [MedicamentoAsignadoInline, AnalisisAsignadoInline]
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('cita', 'paciente', 'doctor', 'estado')
        }),
        ('Información de la Consulta', {
            'fields': ('motivo_consulta', 'sintomas', 'diagnostico', 'observaciones', 'recomendaciones')
        }),
        ('Fechas', {
            'fields': ('fecha_consulta', 'proxima_cita')
        }),
        ('Información del Sistema', {
            'fields': ('creado_por', 'creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MedicamentoAsignado)
class MedicamentoAsignadoAdmin(admin.ModelAdmin):
    list_display = ['medicamento', 'gestion', 'dosis', 'frecuencia', 'estado', 'fecha_prescripcion']
    list_filter = ['estado', 'fecha_prescripcion', 'medicamento']
    search_fields = ['medicamento__nombre', 'gestion__paciente__user__first_name']
    readonly_fields = ['fecha_prescripcion', 'creado_en', 'actualizado_en']

@admin.register(AnalisisAsignado)
class AnalisisAsignadoAdmin(admin.ModelAdmin):
    list_display = ['analisis', 'gestion', 'estado', 'fecha_solicitud', 'fecha_programada']
    list_filter = ['estado', 'fecha_solicitud', 'analisis']
    search_fields = ['analisis__nombre', 'gestion__paciente__user__first_name']
    readonly_fields = ['fecha_solicitud', 'creado_en', 'actualizado_en']

@admin.register(ConfiguracionImpresion)
class ConfiguracionImpresionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'max_elementos_por_impresion', 'nombre_clinica', 'creado_en']
    list_filter = ['activo', 'creado_en']
    search_fields = ['nombre', 'nombre_clinica']
    list_editable = ['activo', 'max_elementos_por_impresion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'activo')
        }),
        ('Archivos de Impresión', {
            'fields': ('archivo_timbrado', 'firma_doctor', 'sello_clinica'),
            'description': 'Sube los archivos PNG necesarios para la impresión'
        }),
        ('Configuración de Impresión', {
            'fields': ('max_elementos_por_impresion',)
        }),
        ('Información de la Clínica', {
            'fields': ('nombre_clinica', 'direccion_clinica', 'telefono_clinica', 'email_clinica')
        }),
        ('Configuración de Página', {
            'fields': ('margen_superior', 'margen_inferior', 'margen_izquierdo', 'margen_derecho'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['creado_en', 'actualizado_en']
    
    def save_model(self, request, obj, form, change):
        # Si este registro se marca como activo, desactivar los demás
        if obj.activo:
            ConfiguracionImpresion.objects.exclude(pk=obj.pk).update(activo=False)
        super().save_model(request, obj, form, change)
