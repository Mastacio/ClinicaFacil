from django.core.management.base import BaseCommand
from gestion.models import Medicamento, Analisis

class Command(BaseCommand):
    help = 'Pobla la base de datos con medicamentos y análisis de ejemplo'

    def handle(self, *args, **options):
        # Crear medicamentos de ejemplo
        medicamentos = [
            {
                'nombre': 'Paracetamol',
                'descripcion': 'Analgésico y antipirético',
                'presentacion': 'Tableta 500mg',
                'dosis_recomendada': '1-2 tabletas cada 4-6 horas'
            },
            {
                'nombre': 'Ibuprofeno',
                'descripcion': 'Antiinflamatorio no esteroideo',
                'presentacion': 'Tableta 400mg',
                'dosis_recomendada': '1 tableta cada 6-8 horas'
            },
            {
                'nombre': 'Amoxicilina',
                'descripcion': 'Antibiótico de amplio espectro',
                'presentacion': 'Cápsula 500mg',
                'dosis_recomendada': '1 cápsula cada 8 horas'
            },
            {
                'nombre': 'Omeprazol',
                'descripcion': 'Protector gástrico',
                'presentacion': 'Cápsula 20mg',
                'dosis_recomendada': '1 cápsula al día'
            },
            {
                'nombre': 'Loratadina',
                'descripcion': 'Antihistamínico',
                'presentacion': 'Tableta 10mg',
                'dosis_recomendada': '1 tableta al día'
            },
            {
                'nombre': 'Metformina',
                'descripcion': 'Antidiabético oral',
                'presentacion': 'Tableta 500mg',
                'dosis_recomendada': '1-2 tabletas al día'
            },
            {
                'nombre': 'Amlodipino',
                'descripcion': 'Antihipertensivo',
                'presentacion': 'Tableta 5mg',
                'dosis_recomendada': '1 tableta al día'
            },
            {
                'nombre': 'Atorvastatina',
                'descripcion': 'Hipolipemiante',
                'presentacion': 'Tableta 20mg',
                'dosis_recomendada': '1 tableta al día'
            }
        ]

        # Crear análisis de ejemplo
        analisis = [
            {
                'nombre': 'Hemograma Completo',
                'descripcion': 'Análisis de sangre que incluye glóbulos rojos, blancos y plaquetas',
                'tipo': 'Hematología',
                'preparacion': 'Ayuno de 8 horas'
            },
            {
                'nombre': 'Glucosa en Sangre',
                'descripcion': 'Medición de niveles de azúcar en sangre',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 12 horas'
            },
            {
                'nombre': 'Perfil Lipídico',
                'descripcion': 'Análisis de colesterol y triglicéridos',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 12 horas'
            },
            {
                'nombre': 'Creatinina',
                'descripcion': 'Función renal',
                'tipo': 'Bioquímica',
                'preparacion': 'Sin preparación especial'
            },
            {
                'nombre': 'TSH',
                'descripcion': 'Hormona estimulante de la tiroides',
                'tipo': 'Hormonal',
                'preparacion': 'Sin preparación especial'
            },
            {
                'nombre': 'Radiografía de Tórax',
                'descripcion': 'Imagen del tórax para evaluar pulmones y corazón',
                'tipo': 'Imagenología',
                'preparacion': 'Sin preparación especial'
            },
            {
                'nombre': 'Electrocardiograma',
                'descripcion': 'Registro de la actividad eléctrica del corazón',
                'tipo': 'Cardiología',
                'preparacion': 'Sin preparación especial'
            },
            {
                'nombre': 'Ecografía Abdominal',
                'descripcion': 'Imagen de los órganos abdominales',
                'tipo': 'Imagenología',
                'preparacion': 'Ayuno de 6 horas'
            }
        ]

        # Crear medicamentos
        for med_data in medicamentos:
            medicamento, created = Medicamento.objects.get_or_create(
                nombre=med_data['nombre'],
                defaults=med_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Medicamento creado: {medicamento.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Medicamento ya existe: {medicamento.nombre}')
                )

        # Crear análisis
        for anal_data in analisis:
            analisis_obj, created = Analisis.objects.get_or_create(
                nombre=anal_data['nombre'],
                defaults=anal_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Análisis creado: {analisis_obj.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Análisis ya existe: {analisis_obj.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS('Datos de ejemplo creados exitosamente')
        ) 