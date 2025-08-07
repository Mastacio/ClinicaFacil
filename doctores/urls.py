from django.urls import path
from .views import (
    gestionar_doctores, crear_doctor, ver_doctor, editar_doctor, activar_desactivar_doctor, 
    agregar_horario, eliminar_horario, gestionar_consultorios, crear_consultorio, 
    ver_consultorio, editar_consultorio, activar_desactivar_consultorio
)

urlpatterns = [
    # URLs para doctores
    path('gestionar/', gestionar_doctores, name='gestionar_doctores'),
    path('crear/', crear_doctor, name='crear_doctor'),
    path('<int:pk>/ver/', ver_doctor, name='ver_doctor'),
    path('<int:pk>/editar/', editar_doctor, name='editar_doctor'),
    path('<int:pk>/activar-desactivar/', activar_desactivar_doctor, name='activar_desactivar_doctor'),
    path('<int:pk>/agregar-horario/', agregar_horario, name='agregar_horario'),
    path('<int:doctor_pk>/eliminar-horario/<int:horario_pk>/', eliminar_horario, name='eliminar_horario'),
    
    # URLs para consultorios
    path('consultorios/', gestionar_consultorios, name='gestionar_consultorios'),
    path('consultorios/crear/', crear_consultorio, name='crear_consultorio'),
    path('consultorios/<int:pk>/ver/', ver_consultorio, name='ver_consultorio'),
    path('consultorios/<int:pk>/editar/', editar_consultorio, name='editar_consultorio'),
    path('consultorios/<int:pk>/activar-desactivar/', activar_desactivar_consultorio, name='activar_desactivar_consultorio'),
]
