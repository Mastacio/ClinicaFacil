from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestionar_citas, name='gestionar_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('crear-modal/', views.crear_cita_modal, name='crear_cita_modal'),
    path('<int:pk>/', views.ver_cita, name='ver_cita'),
    path('<int:pk>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
    path('<int:pk>/confirmar/', views.confirmar_cita, name='confirmar_cita'),
    path('calendario/', views.calendario_doctor, name='calendario_doctor'),
    path('api/buscar_pacientes/', views.api_buscar_pacientes, name='api_buscar_pacientes'),
    path('api/buscar_doctores/', views.api_buscar_doctores, name='api_buscar_doctores'),
    # Nuevas URLs para agenda del doctor
    path('agenda/', views.agenda_doctor, name='agenda_doctor'),
    path('agenda/<int:pk>/cancelar/', views.cancelar_cita_agenda, name='cancelar_cita_agenda'),
    path('agenda/<int:pk>/confirmar/', views.confirmar_cita_agenda, name='confirmar_cita_agenda'),
    # Nuevas URLs para pacientes
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('mis-citas/crear/', views.crear_cita_paciente, name='crear_cita_paciente'),
    path('mis-citas/<int:pk>/cancelar/', views.cancelar_cita_paciente, name='cancelar_cita_paciente'),
    path('mis-citas/<int:pk>/confirmar/', views.confirmar_cita_paciente, name='confirmar_cita_paciente'),
]
