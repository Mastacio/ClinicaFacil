from django.core.management.base import BaseCommand
from gestion.models import ConfiguracionImpresion

class Command(BaseCommand):
    help = 'Pobla la configuración de impresión con datos de ejemplo'

    def handle(self, *args, **options):
        # Crear configuración de impresión por defecto
        config, created = ConfiguracionImpresion.objects.get_or_create(
            nombre='Configuración Principal',
            defaults={
                'activo': True,
                'max_elementos_por_impresion': 3,
                'nombre_clinica': 'CLÍNICA CLINICAFACIL',
                'direccion_clinica': 'Av. Principal 123, Ciudad, País',
                'telefono_clinica': '+1 (555) 123-4567',
                'email_clinica': 'info@clinicafacil.com',
                'margen_superior': 20,
                'margen_inferior': 20,
                'margen_izquierdo': 20,
                'margen_derecho': 20,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Configuración de impresión creada: {config.nombre}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'La configuración ya existe: {config.nombre}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Recuerda subir los archivos de timbrado, firma y sello desde el admin de Django'
            )
        ) 