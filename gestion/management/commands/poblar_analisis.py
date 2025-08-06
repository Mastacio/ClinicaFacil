from django.core.management.base import BaseCommand
from gestion.models import Analisis


class Command(BaseCommand):
    help = 'Pobla la base de datos con análisis médicos comunes'

    def handle(self, *args, **options):
        analisis_data = [
            {
                'nombre': 'Hemograma Completo',
                'descripcion': 'Análisis de sangre que incluye recuento de glóbulos rojos, blancos y plaquetas.',
                'tipo': 'Hematología',
                'preparacion': 'Ayuno de 8-12 horas. No tomar medicamentos sin consultar.'
            },
            {
                'nombre': 'Glucosa en Sangre',
                'descripcion': 'Medición de los niveles de azúcar en sangre para diagnosticar diabetes.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8-12 horas. No comer ni beber excepto agua.'
            },
            {
                'nombre': 'Perfil Lipídico',
                'descripcion': 'Análisis de colesterol total, HDL, LDL y triglicéridos.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 12-14 horas. No consumir alcohol 24 horas antes.'
            },
            {
                'nombre': 'Creatinina',
                'descripcion': 'Medición de la función renal y filtrado glomerular.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. Evitar ejercicio intenso 24 horas antes.'
            },
            {
                'nombre': 'Ácido Úrico',
                'descripcion': 'Medición para diagnosticar gota y evaluar función renal.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. Evitar alimentos ricos en purinas.'
            },
            {
                'nombre': 'Transaminasas (ALT/AST)',
                'descripcion': 'Análisis de función hepática y daño al hígado.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. No consumir alcohol 48 horas antes.'
            },
            {
                'nombre': 'TSH (Hormona Tiroidea)',
                'descripcion': 'Evaluación de la función tiroidea y diagnóstico de hipo/hipertiroidismo.',
                'tipo': 'Hormonal',
                'preparacion': 'Ayuno de 8 horas. Tomar en la mañana temprano.'
            },
            {
                'nombre': 'T4 Libre',
                'descripcion': 'Medición de la hormona tiroidea activa en el organismo.',
                'tipo': 'Hormonal',
                'preparacion': 'Ayuno de 8 horas. Tomar en la mañana temprano.'
            },
            {
                'nombre': 'T3 Libre',
                'descripcion': 'Evaluación de la hormona tiroidea triyodotironina.',
                'tipo': 'Hormonal',
                'preparacion': 'Ayuno de 8 horas. Tomar en la mañana temprano.'
            },
            {
                'nombre': 'Cortisol',
                'descripcion': 'Medición de la hormona del estrés y función adrenal.',
                'tipo': 'Hormonal',
                'preparacion': 'Tomar en la mañana (8-9 AM). Evitar estrés físico.'
            },
            {
                'nombre': 'Insulina',
                'descripcion': 'Evaluación de la producción de insulina y resistencia a la insulina.',
                'tipo': 'Hormonal',
                'preparacion': 'Ayuno de 8-12 horas. No tomar medicamentos para diabetes.'
            },
            {
                'nombre': 'Hemoglobina Glicosilada (HbA1c)',
                'descripcion': 'Control de diabetes a largo plazo (3 meses).',
                'tipo': 'Bioquímica',
                'preparacion': 'No requiere ayuno. Puede tomarse en cualquier momento.'
            },
            {
                'nombre': 'Proteína C Reactiva (PCR)',
                'descripcion': 'Marcador de inflamación e infección en el organismo.',
                'tipo': 'Inmunología',
                'preparacion': 'Ayuno de 8 horas. Evitar infecciones recientes.'
            },
            {
                'nombre': 'Velocidad de Sedimentación (VSG)',
                'descripcion': 'Marcador inespecífico de inflamación y enfermedades autoinmunes.',
                'tipo': 'Hematología',
                'preparacion': 'Ayuno de 8 horas. Evitar ejercicio intenso.'
            },
            {
                'nombre': 'Ferritina',
                'descripcion': 'Evaluación de las reservas de hierro en el organismo.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. No tomar suplementos de hierro.'
            },
            {
                'nombre': 'Vitamina D (25-OH)',
                'descripcion': 'Evaluación de los niveles de vitamina D en sangre.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. Tomar en la mañana.'
            },
            {
                'nombre': 'Vitamina B12',
                'descripcion': 'Evaluación de los niveles de vitamina B12 para anemia.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. No tomar suplementos de B12.'
            },
            {
                'nombre': 'Ácido Fólico',
                'descripcion': 'Evaluación de los niveles de folato en sangre.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. No tomar suplementos de folato.'
            },
            {
                'nombre': 'PSA Total',
                'descripcion': 'Marcador para detección de cáncer de próstata.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No actividad sexual 48 horas antes.'
            },
            {
                'nombre': 'PSA Libre',
                'descripcion': 'Evaluación específica del PSA libre para cáncer de próstata.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No actividad sexual 48 horas antes.'
            },
            {
                'nombre': 'CEA (Antígeno Carcinoembrionario)',
                'descripcion': 'Marcador tumoral para cáncer colorrectal y otros.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No fumar 24 horas antes.'
            },
            {
                'nombre': 'CA 125',
                'descripcion': 'Marcador tumoral para cáncer de ovario.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No durante la menstruación.'
            },
            {
                'nombre': 'CA 19-9',
                'descripcion': 'Marcador tumoral para cáncer de páncreas y tracto digestivo.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No fumar 24 horas antes.'
            },
            {
                'nombre': 'Alfa Fetoproteína (AFP)',
                'descripcion': 'Marcador tumoral para cáncer de hígado y testicular.',
                'tipo': 'Tumorales',
                'preparacion': 'Ayuno de 8 horas. No durante el embarazo.'
            },
            {
                'nombre': 'Beta HCG',
                'descripcion': 'Hormona del embarazo y marcador tumoral.',
                'tipo': 'Hormonal',
                'preparacion': 'Ayuno de 8 horas. No durante el embarazo normal.'
            },
            {
                'nombre': 'Troponina I',
                'descripcion': 'Marcador específico de daño cardíaco e infarto.',
                'tipo': 'Cardiología',
                'preparacion': 'No requiere ayuno. Tomar en emergencias cardíacas.'
            },
            {
                'nombre': 'CPK (Creatina Quinasa)',
                'descripcion': 'Evaluación de daño muscular y cardíaco.',
                'tipo': 'Bioquímica',
                'preparacion': 'Ayuno de 8 horas. Evitar ejercicio intenso 24 horas antes.'
            },
            {
                'nombre': 'BNP (Péptido Natriurético)',
                'descripcion': 'Marcador de insuficiencia cardíaca.',
                'tipo': 'Cardiología',
                'preparacion': 'Ayuno de 8 horas. Evitar estrés físico.'
            },
            {
                'nombre': 'Dímero D',
                'descripcion': 'Marcador de trombosis y embolias pulmonares.',
                'tipo': 'Coagulación',
                'preparacion': 'Ayuno de 8 horas. No tomar anticoagulantes sin consultar.'
            },
            {
                'nombre': 'Tiempo de Protrombina (TP)',
                'descripcion': 'Evaluación de la coagulación sanguínea.',
                'tipo': 'Coagulación',
                'preparacion': 'Ayuno de 8 horas. No tomar anticoagulantes sin consultar.'
            },
            {
                'nombre': 'Tiempo de Tromboplastina (TTP)',
                'descripcion': 'Evaluación de la vía intrínseca de coagulación.',
                'tipo': 'Coagulación',
                'preparacion': 'Ayuno de 8 horas. No tomar anticoagulantes sin consultar.'
            },
            {
                'nombre': 'Fibrinógeno',
                'descripcion': 'Proteína de coagulación y marcador de inflamación.',
                'tipo': 'Coagulación',
                'preparacion': 'Ayuno de 8 horas. Evitar infecciones recientes.'
            },
            {
                'nombre': 'Anticuerpos Antinucleares (ANA)',
                'descripcion': 'Detección de enfermedades autoinmunes como lupus.',
                'tipo': 'Inmunología',
                'preparacion': 'Ayuno de 8 horas. No tomar medicamentos inmunosupresores.'
            },
            {
                'nombre': 'Factor Reumatoideo',
                'descripcion': 'Marcador para artritis reumatoide.',
                'tipo': 'Inmunología',
                'preparacion': 'Ayuno de 8 horas. No tomar medicamentos antiinflamatorios.'
            },
            {
                'nombre': 'Anti CCP',
                'descripcion': 'Anticuerpos específicos para artritis reumatoide.',
                'tipo': 'Inmunología',
                'preparacion': 'Ayuno de 8 horas. No tomar medicamentos antiinflamatorios.'
            },
            {
                'nombre': 'Hepatitis B (HBsAg)',
                'descripcion': 'Detección de antígeno de superficie de hepatitis B.',
                'tipo': 'Infecciosas',
                'preparacion': 'Ayuno de 8 horas. No requiere preparación especial.'
            },
            {
                'nombre': 'Hepatitis C (Anti HCV)',
                'descripcion': 'Detección de anticuerpos contra hepatitis C.',
                'tipo': 'Infecciosas',
                'preparacion': 'Ayuno de 8 horas. No requiere preparación especial.'
            },
            {
                'nombre': 'VIH (Anticuerpos)',
                'descripcion': 'Detección de anticuerpos contra el virus del VIH.',
                'tipo': 'Infecciosas',
                'preparacion': 'Ayuno de 8 horas. Consentimiento informado requerido.'
            },
            {
                'nombre': 'VDRL/RPR',
                'descripcion': 'Prueba de detección de sífilis.',
                'tipo': 'Infecciosas',
                'preparacion': 'Ayuno de 8 horas. No requiere preparación especial.'
            },
            {
                'nombre': 'Cultivo de Orina',
                'descripcion': 'Detección de bacterias en orina y sensibilidad a antibióticos.',
                'tipo': 'Microbiología',
                'preparacion': 'Lavar genitales. Tomar muestra de orina media.'
            },
            {
                'nombre': 'Cultivo de Esputo',
                'descripcion': 'Detección de bacterias en secreciones respiratorias.',
                'tipo': 'Microbiología',
                'preparacion': 'Enjuagar boca. Tomar muestra de esputo matutino.'
            },
            {
                'nombre': 'Cultivo de Sangre',
                'descripcion': 'Detección de bacterias en sangre (septicemia).',
                'tipo': 'Microbiología',
                'preparacion': 'No requiere ayuno. Tomar durante episodio febril.'
            },
            {
                'nombre': 'Examen General de Orina',
                'descripcion': 'Evaluación completa de la orina para detectar enfermedades.',
                'tipo': 'Bioquímica',
                'preparacion': 'Lavar genitales. Tomar muestra de orina media.'
            },
            {
                'nombre': 'Microalbuminuria',
                'descripcion': 'Detección temprana de daño renal en diabéticos.',
                'tipo': 'Bioquímica',
                'preparacion': 'Recolectar orina de 24 horas. Mantener refrigerada.'
            },
            {
                'nombre': 'Creatinina en Orina',
                'descripcion': 'Evaluación de la función renal mediante orina.',
                'tipo': 'Bioquímica',
                'preparacion': 'Recolectar orina de 24 horas. Mantener refrigerada.'
            },
            {
                'nombre': 'Urocultivo',
                'descripcion': 'Cultivo bacteriano de orina para infecciones urinarias.',
                'tipo': 'Microbiología',
                'preparacion': 'Lavar genitales. Tomar muestra de orina media.'
            },
            {
                'nombre': 'Citología Cervical (Papanicolaou)',
                'descripcion': 'Detección temprana de cáncer de cuello uterino.',
                'tipo': 'Citología',
                'preparacion': 'No durante menstruación. No relaciones sexuales 48 horas antes.'
            },
            {
                'nombre': 'Biopsia de Piel',
                'descripcion': 'Análisis de tejido cutáneo para diagnóstico dermatológico.',
                'tipo': 'Anatomía Patológica',
                'preparacion': 'No requiere ayuno. Limpiar área a biopsiar.'
            },
            {
                'nombre': 'Biopsia de Mama',
                'descripcion': 'Análisis de tejido mamario para diagnóstico de cáncer.',
                'tipo': 'Anatomía Patológica',
                'preparacion': 'No requiere ayuno. No usar desodorante el día del estudio.'
            },
            {
                'nombre': 'Endoscopia Digestiva Alta',
                'descripcion': 'Visualización del esófago, estómago y duodeno.',
                'tipo': 'Endoscopia',
                'preparacion': 'Ayuno de 8 horas. No tomar medicamentos sin consultar.'
            },
            {
                'nombre': 'Colonoscopia',
                'descripcion': 'Visualización del colon y recto para detección de cáncer.',
                'tipo': 'Endoscopia',
                'preparacion': 'Dieta líquida 24 horas antes. Preparación intestinal.'
            },
            {
                'nombre': 'Radiografía de Tórax',
                'descripcion': 'Imagen del tórax para evaluar pulmones y corazón.',
                'tipo': 'Radiología',
                'preparacion': 'No requiere ayuno. Quitar objetos metálicos.'
            },
            {
                'nombre': 'Tomografía Computarizada',
                'descripcion': 'Imagen tridimensional de diferentes partes del cuerpo.',
                'tipo': 'Radiología',
                'preparacion': 'Ayuno de 4-6 horas. No usar objetos metálicos.'
            },
            {
                'nombre': 'Resonancia Magnética',
                'descripcion': 'Imagen detallada usando campos magnéticos.',
                'tipo': 'Radiología',
                'preparacion': 'No requiere ayuno. No usar objetos metálicos.'
            },
            {
                'nombre': 'Ecografía Abdominal',
                'descripcion': 'Imagen de órganos abdominales usando ultrasonido.',
                'tipo': 'Radiología',
                'preparacion': 'Ayuno de 6-8 horas. Beber agua para llenar vejiga.'
            },
            {
                'nombre': 'Electrocardiograma (ECG)',
                'descripcion': 'Registro de la actividad eléctrica del corazón.',
                'tipo': 'Cardiología',
                'preparacion': 'No requiere ayuno. Relajarse antes del estudio.'
            },
            {
                'nombre': 'Ecocardiograma',
                'descripcion': 'Imagen del corazón usando ultrasonido.',
                'tipo': 'Cardiología',
                'preparacion': 'No requiere ayuno. Relajarse antes del estudio.'
            },
            {
                'nombre': 'Prueba de Esfuerzo',
                'descripcion': 'Evaluación cardíaca durante ejercicio físico.',
                'tipo': 'Cardiología',
                'preparacion': 'Ayuno de 4 horas. Usar ropa cómoda para ejercicio.'
            },
            {
                'nombre': 'Holter de 24 Horas',
                'descripcion': 'Monitoreo continuo del ritmo cardíaco.',
                'tipo': 'Cardiología',
                'preparacion': 'No requiere ayuno. Mantener actividad normal.'
            },
            {
                'nombre': 'Espirometría',
                'descripcion': 'Evaluación de la función pulmonar.',
                'tipo': 'Neumología',
                'preparacion': 'No fumar 24 horas antes. No usar broncodilatadores.'
            },
            {
                'nombre': 'Polisomnografía',
                'descripcion': 'Estudio del sueño para diagnosticar trastornos.',
                'tipo': 'Neurología',
                'preparacion': 'No dormir siesta el día anterior. Llevar pijama cómodo.'
            },
            {
                'nombre': 'Electroencefalograma (EEG)',
                'descripcion': 'Registro de la actividad eléctrica cerebral.',
                'tipo': 'Neurología',
                'preparacion': 'No requiere ayuno. Dormir bien la noche anterior.'
            },
            {
                'nombre': 'Densitometría Ósea',
                'descripcion': 'Evaluación de la densidad mineral ósea.',
                'tipo': 'Radiología',
                'preparacion': 'No requiere ayuno. No tomar suplementos de calcio.'
            },
            {
                'nombre': 'Mamografía',
                'descripcion': 'Radiografía de las mamas para detección de cáncer.',
                'tipo': 'Radiología',
                'preparacion': 'No usar desodorante. Programar fuera de menstruación.'
            }
        ]

        analisis_creados = 0
        analisis_existentes = 0

        for analisis_data in analisis_data:
            analisis, created = Analisis.objects.get_or_create(
                nombre=analisis_data['nombre'],
                defaults={
                    'descripcion': analisis_data['descripcion'],
                    'tipo': analisis_data['tipo'],
                    'preparacion': analisis_data['preparacion']
                }
            )
            
            if created:
                analisis_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Análisis creado: {analisis.nombre}')
                )
            else:
                analisis_existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Análisis ya existe: {analisis.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado:\n'
                f'   • Análisis creados: {analisis_creados}\n'
                f'   • Análisis existentes: {analisis_existentes}\n'
                f'   • Total de análisis: {analisis_creados + analisis_existentes}'
            )
        ) 