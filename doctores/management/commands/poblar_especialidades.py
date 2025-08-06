from django.core.management.base import BaseCommand
from doctores.models import Especialidad


class Command(BaseCommand):
    help = 'Pobla la base de datos con especialidades médicas comunes'

    def handle(self, *args, **options):
        especialidades_data = [
            {
                'nombre': 'Medicina General',
                'descripcion': 'Atención médica integral para pacientes de todas las edades, incluyendo diagnóstico, tratamiento y prevención de enfermedades comunes.'
            },
            {
                'nombre': 'Cardiología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del corazón y del sistema circulatorio.'
            },
            {
                'nombre': 'Dermatología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades de la piel, cabello y uñas.'
            },
            {
                'nombre': 'Endocrinología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades relacionadas con las hormonas y el metabolismo.'
            },
            {
                'nombre': 'Gastroenterología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del aparato digestivo.'
            },
            {
                'nombre': 'Ginecología y Obstetricia',
                'descripcion': 'Especialidad médica que se encarga de la salud reproductiva de la mujer, incluyendo embarazo, parto y enfermedades ginecológicas.'
            },
            {
                'nombre': 'Hematología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades de la sangre y órganos hematopoyéticos.'
            },
            {
                'nombre': 'Infectología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades infecciosas.'
            },
            {
                'nombre': 'Medicina Interna',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de enfermedades en adultos, con enfoque en medicina general avanzada.'
            },
            {
                'nombre': 'Nefrología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de los riñones.'
            },
            {
                'nombre': 'Neurología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del sistema nervioso.'
            },
            {
                'nombre': 'Oftalmología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de los ojos.'
            },
            {
                'nombre': 'Oncología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento del cáncer.'
            },
            {
                'nombre': 'Ortopedia y Traumatología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades y lesiones del sistema musculoesquelético.'
            },
            {
                'nombre': 'Otorrinolaringología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del oído, nariz y garganta.'
            },
            {
                'nombre': 'Patología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico de enfermedades mediante el examen de tejidos y células.'
            },
            {
                'nombre': 'Pediatría',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades en niños y adolescentes.'
            },
            {
                'nombre': 'Neumología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del sistema respiratorio.'
            },
            {
                'nombre': 'Psiquiatría',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades mentales y trastornos del comportamiento.'
            },
            {
                'nombre': 'Radiología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico mediante técnicas de imagen médica.'
            },
            {
                'nombre': 'Reumatología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades reumáticas y autoinmunes.'
            },
            {
                'nombre': 'Urología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del sistema urinario y genital masculino.'
            },
            {
                'nombre': 'Anestesiología',
                'descripcion': 'Especialidad médica que se encarga de la anestesia y el manejo del dolor durante procedimientos quirúrgicos.'
            },
            {
                'nombre': 'Cirugía General',
                'descripcion': 'Especialidad médica que se ocupa de procedimientos quirúrgicos en diferentes partes del cuerpo.'
            },
            {
                'nombre': 'Cirugía Cardiovascular',
                'descripcion': 'Especialidad médica que se encarga de procedimientos quirúrgicos en el corazón y vasos sanguíneos.'
            },
            {
                'nombre': 'Cirugía Plástica',
                'descripcion': 'Especialidad médica que se ocupa de procedimientos reconstructivos y estéticos.'
            },
            {
                'nombre': 'Medicina de Emergencias',
                'descripcion': 'Especialidad médica que se encarga de la atención médica inmediata en situaciones de emergencia.'
            },
            {
                'nombre': 'Medicina Familiar',
                'descripcion': 'Especialidad médica que proporciona atención integral y continua a individuos y familias.'
            },
            {
                'nombre': 'Medicina Preventiva',
                'descripcion': 'Especialidad médica que se enfoca en la prevención de enfermedades y promoción de la salud.'
            },
            {
                'nombre': 'Nutriología',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de problemas nutricionales.'
            },
            {
                'nombre': 'Alergología',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y tratamiento de las alergias y enfermedades alérgicas.'
            },
            {
                'nombre': 'Inmunología',
                'descripcion': 'Especialidad médica que se encarga del estudio del sistema inmunológico y sus trastornos.'
            },
            {
                'nombre': 'Genética Médica',
                'descripcion': 'Especialidad médica que se ocupa del diagnóstico y asesoramiento de enfermedades genéticas.'
            },
            {
                'nombre': 'Medicina del Deporte',
                'descripcion': 'Especialidad médica que se encarga de la salud y el rendimiento de los deportistas.'
            },
            {
                'nombre': 'Medicina del Trabajo',
                'descripcion': 'Especialidad médica que se ocupa de la salud en el entorno laboral.'
            },
            {
                'nombre': 'Geriatría',
                'descripcion': 'Especialidad médica que se encarga de la atención médica de personas mayores.'
            },
            {
                'nombre': 'Medicina Crítica',
                'descripcion': 'Especialidad médica que se encarga de la atención de pacientes en estado crítico.'
            },
            {
                'nombre': 'Medicina Nuclear',
                'descripcion': 'Especialidad médica que utiliza técnicas de medicina nuclear para diagnóstico y tratamiento.'
            },
            {
                'nombre': 'Fisiatría',
                'descripcion': 'Especialidad médica que se encarga de la rehabilitación física y funcional.'
            },
            {
                'nombre': 'Medicina Paliativa',
                'descripcion': 'Especialidad médica que se encarga del cuidado paliativo y control de síntomas.'
            },
            {
                'nombre': 'Medicina del Dolor',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento del dolor crónico.'
            },
            {
                'nombre': 'Medicina del Sueño',
                'descripcion': 'Especialidad médica que se encarga del diagnóstico y tratamiento de trastornos del sueño.'
            },
            {
                'nombre': 'Medicina Estética',
                'descripcion': 'Especialidad médica que se encarga de procedimientos estéticos no quirúrgicos.'
            },
            {
                'nombre': 'Medicina Integrativa',
                'descripcion': 'Especialidad médica que combina medicina convencional con terapias complementarias.'
            },
            {
                'nombre': 'Medicina Funcional',
                'descripcion': 'Especialidad médica que se enfoca en la causa raíz de las enfermedades.'
            },
            {
                'nombre': 'Medicina Regenerativa',
                'descripcion': 'Especialidad médica que utiliza terapias regenerativas para tratar enfermedades.'
            },
            {
                'nombre': 'Medicina Personalizada',
                'descripcion': 'Especialidad médica que adapta el tratamiento según las características individuales del paciente.'
            }
        ]

        especialidades_creadas = 0
        especialidades_existentes = 0

        for especialidad_data in especialidades_data:
            especialidad, created = Especialidad.objects.get_or_create(
                nombre=especialidad_data['nombre'],
                defaults={'descripcion': especialidad_data['descripcion']}
            )
            
            if created:
                especialidades_creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Especialidad creada: {especialidad.nombre}')
                )
            else:
                especialidades_existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Especialidad ya existe: {especialidad.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado:\n'
                f'   • Especialidades creadas: {especialidades_creadas}\n'
                f'   • Especialidades existentes: {especialidades_existentes}\n'
                f'   • Total de especialidades: {especialidades_creadas + especialidades_existentes}'
            )
        ) 