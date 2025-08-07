from django.core.management.base import BaseCommand
from doctores.models import Consultorio


class Command(BaseCommand):
    help = 'Pobla la base de datos con consultorios por defecto'

    def handle(self, *args, **options):
        consultorios_data = [
            {
                'nombre': 'Consultorio 1',
                'descripcion': 'Consultorio principal para atención general',
                'ubicacion': 'Primer piso, ala norte',
                'capacidad': 1,
                'activo': True
            },
            {
                'nombre': 'Consultorio 2',
                'descripcion': 'Consultorio para especialidades',
                'ubicacion': 'Primer piso, ala sur',
                'capacidad': 1,
                'activo': True
            },
            {
                'nombre': 'Consultorio 3',
                'descripcion': 'Consultorio para pediatría',
                'ubicacion': 'Segundo piso, ala norte',
                'capacidad': 1,
                'activo': True
            },
            {
                'nombre': 'Consultorio 4',
                'descripcion': 'Consultorio para ginecología',
                'ubicacion': 'Segundo piso, ala sur',
                'capacidad': 1,
                'activo': True
            },
            {
                'nombre': 'Sala de Emergencias',
                'descripcion': 'Sala para atención de emergencias',
                'ubicacion': 'Planta baja, ala este',
                'capacidad': 2,
                'activo': True
            }
        ]

        for data in consultorios_data:
            consultorio, created = Consultorio.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Consultorio "{consultorio.nombre}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Consultorio "{consultorio.nombre}" ya existe')
                )

        self.stdout.write(
            self.style.SUCCESS('Proceso de poblamiento de consultorios completado')
        ) 