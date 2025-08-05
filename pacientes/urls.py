
from django.urls import path
from .views import completar_perfil, crear_paciente, gestionar_pacientes, ver_paciente, editar_paciente, activar_desactivar_paciente

urlpatterns = [
    path('completar-perfil/', completar_perfil, name='completar_perfil'),
    path('crear/', crear_paciente, name='crear_paciente'),
    path('gestionar/', gestionar_pacientes, name='gestionar_pacientes'),
    path('<int:pk>/ver/', ver_paciente, name='ver_paciente'),
    path('<int:pk>/editar/', editar_paciente, name='editar_paciente'),
    path('<int:pk>/activar-desactivar/', activar_desactivar_paciente, name='activar_desactivar_paciente'),
]
