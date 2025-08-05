from django.urls import path
from .views import gestionar_doctores, crear_doctor, ver_doctor, editar_doctor, activar_desactivar_doctor, agregar_horario, eliminar_horario

urlpatterns = [
    path('gestionar/', gestionar_doctores, name='gestionar_doctores'),
    path('crear/', crear_doctor, name='crear_doctor'),
    path('<int:pk>/ver/', ver_doctor, name='ver_doctor'),
    path('<int:pk>/editar/', editar_doctor, name='editar_doctor'),
    path('<int:pk>/activar-desactivar/', activar_desactivar_doctor, name='activar_desactivar_doctor'),
    path('<int:pk>/agregar-horario/', agregar_horario, name='agregar_horario'),
    path('<int:doctor_pk>/eliminar-horario/<int:horario_pk>/', eliminar_horario, name='eliminar_horario'),
]
