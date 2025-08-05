from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Gestión principal de citas
    path('cita/<int:cita_id>/', views.gestionar_cita, name='gestionar_cita'),
    
    # Gestión de medicamentos
    path('gestion/<int:gestion_id>/agregar-medicamento/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamento/<int:medicamento_id>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('medicamento/<int:medicamento_id>/cambiar-estado/', views.cambiar_estado_medicamento, name='cambiar_estado_medicamento'),
    
    # Gestión de análisis
    path('gestion/<int:gestion_id>/agregar-analisis/', views.agregar_analisis, name='agregar_analisis'),
    path('analisis/<int:analisis_id>/eliminar/', views.eliminar_analisis, name='eliminar_analisis'),
    path('analisis/<int:analisis_id>/cambiar-estado/', views.cambiar_estado_analisis, name='cambiar_estado_analisis'),
    
    # Impresión
    path('gestion/<int:gestion_id>/imprimir-prescripcion/', views.imprimir_prescripcion, name='imprimir_prescripcion'),
    path('gestion/<int:gestion_id>/imprimir-analisis/', views.imprimir_analisis, name='imprimir_analisis'),
] 