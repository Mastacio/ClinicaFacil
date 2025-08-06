from django.core.management.base import BaseCommand
from gestion.models import Medicamento


class Command(BaseCommand):
    help = 'Pobla la base de datos con medicamentos comunes'

    def handle(self, *args, **options):
        medicamentos_data = [
            {
                'nombre': 'Paracetamol',
                'descripcion': 'Analgésico y antipirético utilizado para tratar el dolor y la fiebre.',
                'presentacion': 'Tabletas 500mg',
                'dosis_recomendada': '500-1000mg cada 4-6 horas'
            },
            {
                'nombre': 'Ibuprofeno',
                'descripcion': 'Antiinflamatorio no esteroideo (AINE) para dolor, inflamación y fiebre.',
                'presentacion': 'Tabletas 400mg, 600mg',
                'dosis_recomendada': '400-600mg cada 6-8 horas'
            },
            {
                'nombre': 'Amoxicilina',
                'descripcion': 'Antibiótico de la familia de las penicilinas para tratar infecciones bacterianas.',
                'presentacion': 'Cápsulas 500mg, Suspensión 250mg/5ml',
                'dosis_recomendada': '500mg cada 8 horas'
            },
            {
                'nombre': 'Omeprazol',
                'descripcion': 'Inhibidor de la bomba de protones para tratar úlceras y reflujo gastroesofágico.',
                'presentacion': 'Cápsulas 20mg',
                'dosis_recomendada': '20mg una vez al día'
            },
            {
                'nombre': 'Loratadina',
                'descripcion': 'Antihistamínico para tratar síntomas de alergias.',
                'presentacion': 'Tabletas 10mg',
                'dosis_recomendada': '10mg una vez al día'
            },
            {
                'nombre': 'Metformina',
                'descripcion': 'Medicamento antidiabético oral para tratar la diabetes tipo 2.',
                'presentacion': 'Tabletas 500mg, 850mg, 1000mg',
                'dosis_recomendada': '500-1000mg dos veces al día'
            },
            {
                'nombre': 'Losartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para tratar hipertensión arterial.',
                'presentacion': 'Tabletas 50mg, 100mg',
                'dosis_recomendada': '50-100mg una vez al día'
            },
            {
                'nombre': 'Atorvastatina',
                'descripcion': 'Estatina para reducir el colesterol y prevenir enfermedades cardiovasculares.',
                'presentacion': 'Tabletas 10mg, 20mg, 40mg',
                'dosis_recomendada': '10-40mg una vez al día'
            },
            {
                'nombre': 'Amlodipino',
                'descripcion': 'Bloqueador de canales de calcio para tratar hipertensión arterial.',
                'presentacion': 'Tabletas 5mg, 10mg',
                'dosis_recomendada': '5-10mg una vez al día'
            },
            {
                'nombre': 'Sertralina',
                'descripcion': 'Antidepresivo inhibidor selectivo de la recaptación de serotonina (ISRS).',
                'presentacion': 'Tabletas 50mg, 100mg',
                'dosis_recomendada': '50-200mg una vez al día'
            },
            {
                'nombre': 'Alprazolam',
                'descripcion': 'Benzodiacepina para tratar ansiedad y trastornos de pánico.',
                'presentacion': 'Tabletas 0.25mg, 0.5mg, 1mg',
                'dosis_recomendada': '0.25-1mg tres veces al día'
            },
            {
                'nombre': 'Diclofenaco',
                'descripcion': 'Antiinflamatorio no esteroideo para dolor e inflamación.',
                'presentacion': 'Tabletas 50mg, Gel tópico',
                'dosis_recomendada': '50mg dos veces al día'
            },
            {
                'nombre': 'Ciprofloxacino',
                'descripcion': 'Antibiótico fluoroquinolona para infecciones bacterianas.',
                'presentacion': 'Tabletas 500mg, 750mg',
                'dosis_recomendada': '500-750mg dos veces al día'
            },
            {
                'nombre': 'Pantoprazol',
                'descripcion': 'Inhibidor de la bomba de protones para úlceras y reflujo.',
                'presentacion': 'Tabletas 40mg',
                'dosis_recomendada': '40mg una vez al día'
            },
            {
                'nombre': 'Cetirizina',
                'descripcion': 'Antihistamínico para síntomas de alergias.',
                'presentacion': 'Tabletas 10mg, Jarabe 5mg/5ml',
                'dosis_recomendada': '10mg una vez al día'
            },
            {
                'nombre': 'Glimepirida',
                'descripcion': 'Sulfonilurea para tratar diabetes tipo 2.',
                'presentacion': 'Tabletas 1mg, 2mg, 4mg',
                'dosis_recomendada': '1-4mg una vez al día'
            },
            {
                'nombre': 'Valsartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para hipertensión.',
                'presentacion': 'Tabletas 80mg, 160mg',
                'dosis_recomendada': '80-160mg una vez al día'
            },
            {
                'nombre': 'Simvastatina',
                'descripcion': 'Estatina para reducir colesterol.',
                'presentacion': 'Tabletas 10mg, 20mg, 40mg',
                'dosis_recomendada': '10-40mg una vez al día'
            },
            {
                'nombre': 'Diltiazem',
                'descripcion': 'Bloqueador de canales de calcio para hipertensión y angina.',
                'presentacion': 'Tabletas 60mg, 90mg, 120mg',
                'dosis_recomendada': '60-120mg tres veces al día'
            },
            {
                'nombre': 'Fluoxetina',
                'descripcion': 'Antidepresivo ISRS para depresión y trastornos obsesivo-compulsivos.',
                'presentacion': 'Cápsulas 20mg',
                'dosis_recomendada': '20mg una vez al día'
            },
            {
                'nombre': 'Clonazepam',
                'descripcion': 'Benzodiacepina para epilepsia y trastornos de ansiedad.',
                'presentacion': 'Tabletas 0.5mg, 1mg, 2mg',
                'dosis_recomendada': '0.5-2mg dos veces al día'
            },
            {
                'nombre': 'Naproxeno',
                'descripcion': 'Antiinflamatorio no esteroideo para dolor e inflamación.',
                'presentacion': 'Tabletas 250mg, 500mg',
                'dosis_recomendada': '250-500mg dos veces al día'
            },
            {
                'nombre': 'Azitromicina',
                'descripcion': 'Antibiótico macrólido para infecciones respiratorias.',
                'presentacion': 'Tabletas 500mg, Suspensión 200mg/5ml',
                'dosis_recomendada': '500mg una vez al día por 3 días'
            },
            {
                'nombre': 'Esomeprazol',
                'descripcion': 'Inhibidor de la bomba de protones para úlceras y reflujo.',
                'presentacion': 'Cápsulas 20mg, 40mg',
                'dosis_recomendada': '20-40mg una vez al día'
            },
            {
                'nombre': 'Fexofenadina',
                'descripcion': 'Antihistamínico no sedante para alergias.',
                'presentacion': 'Tabletas 120mg, 180mg',
                'dosis_recomendada': '120-180mg una vez al día'
            },
            {
                'nombre': 'Pioglitazona',
                'descripcion': 'Tiazolidinediona para tratar diabetes tipo 2.',
                'presentacion': 'Tabletas 15mg, 30mg, 45mg',
                'dosis_recomendada': '15-45mg una vez al día'
            },
            {
                'nombre': 'Irbesartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para hipertensión.',
                'presentacion': 'Tabletas 150mg, 300mg',
                'dosis_recomendada': '150-300mg una vez al día'
            },
            {
                'nombre': 'Pravastatina',
                'descripcion': 'Estatina para reducir colesterol.',
                'presentacion': 'Tabletas 10mg, 20mg, 40mg',
                'dosis_recomendada': '10-40mg una vez al día'
            },
            {
                'nombre': 'Verapamilo',
                'descripcion': 'Bloqueador de canales de calcio para hipertensión y angina.',
                'presentacion': 'Tabletas 80mg, 120mg',
                'dosis_recomendada': '80-120mg tres veces al día'
            },
            {
                'nombre': 'Sertralina',
                'descripcion': 'Antidepresivo ISRS para depresión y trastornos de ansiedad.',
                'presentacion': 'Tabletas 50mg, 100mg',
                'dosis_recomendada': '50-200mg una vez al día'
            },
            {
                'nombre': 'Diazepam',
                'descripcion': 'Benzodiacepina para ansiedad, espasmos musculares y convulsiones.',
                'presentacion': 'Tabletas 5mg, 10mg',
                'dosis_recomendada': '5-10mg dos veces al día'
            },
            {
                'nombre': 'Ketorolaco',
                'descripcion': 'Antiinflamatorio no esteroideo para dolor agudo.',
                'presentacion': 'Tabletas 10mg, Inyección 30mg/ml',
                'dosis_recomendada': '10mg cada 4-6 horas'
            },
            {
                'nombre': 'Claritromicina',
                'descripcion': 'Antibiótico macrólido para infecciones respiratorias.',
                'presentacion': 'Tabletas 250mg, 500mg',
                'dosis_recomendada': '250-500mg dos veces al día'
            },
            {
                'nombre': 'Lansoprazol',
                'descripcion': 'Inhibidor de la bomba de protones para úlceras y reflujo.',
                'presentacion': 'Cápsulas 15mg, 30mg',
                'dosis_recomendada': '15-30mg una vez al día'
            },
            {
                'nombre': 'Desloratadina',
                'descripcion': 'Antihistamínico no sedante para alergias.',
                'presentacion': 'Tabletas 5mg',
                'dosis_recomendada': '5mg una vez al día'
            },
            {
                'nombre': 'Sitagliptina',
                'descripcion': 'Inhibidor de la DPP-4 para tratar diabetes tipo 2.',
                'presentacion': 'Tabletas 50mg, 100mg',
                'dosis_recomendada': '50-100mg una vez al día'
            },
            {
                'nombre': 'Candesartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para hipertensión.',
                'presentacion': 'Tabletas 4mg, 8mg, 16mg',
                'dosis_recomendada': '4-16mg una vez al día'
            },
            {
                'nombre': 'Rosuvastatina',
                'descripcion': 'Estatina para reducir colesterol.',
                'presentacion': 'Tabletas 5mg, 10mg, 20mg',
                'dosis_recomendada': '5-20mg una vez al día'
            },
            {
                'nombre': 'Nifedipino',
                'descripcion': 'Bloqueador de canales de calcio para hipertensión y angina.',
                'presentacion': 'Tabletas 10mg, 20mg',
                'dosis_recomendada': '10-20mg tres veces al día'
            },
            {
                'nombre': 'Venlafaxina',
                'descripcion': 'Antidepresivo inhibidor de la recaptación de serotonina y noradrenalina.',
                'presentacion': 'Cápsulas 37.5mg, 75mg, 150mg',
                'dosis_recomendada': '75-225mg una vez al día'
            },
            {
                'nombre': 'Lorazepam',
                'descripcion': 'Benzodiacepina para ansiedad y convulsiones.',
                'presentacion': 'Tabletas 0.5mg, 1mg, 2mg',
                'dosis_recomendada': '0.5-2mg dos veces al día'
            },
            {
                'nombre': 'Meloxicam',
                'descripcion': 'Antiinflamatorio no esteroideo para dolor e inflamación.',
                'presentacion': 'Tabletas 7.5mg, 15mg',
                'dosis_recomendada': '7.5-15mg una vez al día'
            },
            {
                'nombre': 'Doxiciclina',
                'descripcion': 'Antibiótico tetraciclina para infecciones bacterianas.',
                'presentacion': 'Cápsulas 100mg',
                'dosis_recomendada': '100mg dos veces al día'
            },
            {
                'nombre': 'Rabeprazol',
                'descripcion': 'Inhibidor de la bomba de protones para úlceras y reflujo.',
                'presentacion': 'Tabletas 20mg',
                'dosis_recomendada': '20mg una vez al día'
            },
            {
                'nombre': 'Levocetirizina',
                'descripcion': 'Antihistamínico no sedante para alergias.',
                'presentacion': 'Tabletas 5mg',
                'dosis_recomendada': '5mg una vez al día'
            },
            {
                'nombre': 'Linagliptina',
                'descripcion': 'Inhibidor de la DPP-4 para tratar diabetes tipo 2.',
                'presentacion': 'Tabletas 5mg',
                'dosis_recomendada': '5mg una vez al día'
            },
            {
                'nombre': 'Olmesartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para hipertensión.',
                'presentacion': 'Tabletas 20mg, 40mg',
                'dosis_recomendada': '20-40mg una vez al día'
            },
            {
                'nombre': 'Pitavastatina',
                'descripcion': 'Estatina para reducir colesterol.',
                'presentacion': 'Tabletas 1mg, 2mg, 4mg',
                'dosis_recomendada': '1-4mg una vez al día'
            },
            {
                'nombre': 'Amlodipino + Valsartán',
                'descripcion': 'Combinación de bloqueador de canales de calcio y antagonista de angiotensina II.',
                'presentacion': 'Tabletas 5/80mg, 5/160mg, 10/160mg',
                'dosis_recomendada': 'Una tableta una vez al día'
            },
            {
                'nombre': 'Duloxetina',
                'descripcion': 'Antidepresivo inhibidor de la recaptación de serotonina y noradrenalina.',
                'presentacion': 'Cápsulas 30mg, 60mg',
                'dosis_recomendada': '30-60mg una vez al día'
            },
            {
                'nombre': 'Bromazepam',
                'descripcion': 'Benzodiacepina para ansiedad y trastornos del sueño.',
                'presentacion': 'Tabletas 3mg, 6mg',
                'dosis_recomendada': '3-6mg dos veces al día'
            },
            {
                'nombre': 'Celecoxib',
                'descripcion': 'Antiinflamatorio no esteroideo selectivo para dolor e inflamación.',
                'presentacion': 'Cápsulas 100mg, 200mg',
                'dosis_recomendada': '100-200mg dos veces al día'
            },
            {
                'nombre': 'Minociclina',
                'descripcion': 'Antibiótico tetraciclina para infecciones bacterianas.',
                'presentacion': 'Cápsulas 50mg, 100mg',
                'dosis_recomendada': '50-100mg dos veces al día'
            },
            {
                'nombre': 'Dexlansoprazol',
                'descripcion': 'Inhibidor de la bomba de protones para úlceras y reflujo.',
                'presentacion': 'Cápsulas 30mg, 60mg',
                'dosis_recomendada': '30-60mg una vez al día'
            },
            {
                'nombre': 'Rupatadina',
                'descripcion': 'Antihistamínico para síntomas de alergias.',
                'presentacion': 'Tabletas 10mg',
                'dosis_recomendada': '10mg una vez al día'
            },
            {
                'nombre': 'Saxagliptina',
                'descripcion': 'Inhibidor de la DPP-4 para tratar diabetes tipo 2.',
                'presentacion': 'Tabletas 2.5mg, 5mg',
                'dosis_recomendada': '2.5-5mg una vez al día'
            },
            {
                'nombre': 'Telmisartán',
                'descripcion': 'Antagonista del receptor de angiotensina II para hipertensión.',
                'presentacion': 'Tabletas 20mg, 40mg, 80mg',
                'dosis_recomendada': '20-80mg una vez al día'
            },
            {
                'nombre': 'Fluvastatina',
                'descripcion': 'Estatina para reducir colesterol.',
                'presentacion': 'Cápsulas 20mg, 40mg',
                'dosis_recomendada': '20-40mg una vez al día'
            }
        ]

        medicamentos_creados = 0
        medicamentos_existentes = 0

        for medicamento_data in medicamentos_data:
            medicamento, created = Medicamento.objects.get_or_create(
                nombre=medicamento_data['nombre'],
                defaults={
                    'descripcion': medicamento_data['descripcion'],
                    'presentacion': medicamento_data['presentacion'],
                    'dosis_recomendada': medicamento_data['dosis_recomendada']
                }
            )
            
            if created:
                medicamentos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Medicamento creado: {medicamento.nombre}')
                )
            else:
                medicamentos_existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Medicamento ya existe: {medicamento.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado:\n'
                f'   • Medicamentos creados: {medicamentos_creados}\n'
                f'   • Medicamentos existentes: {medicamentos_existentes}\n'
                f'   • Total de medicamentos: {medicamentos_creados + medicamentos_existentes}'
            )
        ) 