from django import forms
from .models import GestionCita, MedicamentoAsignado, AnalisisAsignado

class GestionCitaForm(forms.ModelForm):
    """
    Formulario para gestionar una cita
    """
    class Meta:
        model = GestionCita
        fields = [
            'motivo_consulta', 'sintomas', 'diagnostico', 
            'observaciones', 'recomendaciones', 'estado', 'proxima_cita'
        ]
        widgets = {
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el motivo de la consulta...'
            }),
            'sintomas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa los síntomas del paciente...'
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnóstico médico...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
            'recomendaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Recomendaciones para el paciente...'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proxima_cita': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class MedicamentoAsignadoForm(forms.ModelForm):
    """
    Formulario para asignar medicamentos
    """
    class Meta:
        model = MedicamentoAsignado
        fields = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'medicamento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 tableta, 500mg'
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas, 2 veces al día'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 7 días, 2 semanas'
            }),
            'instrucciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Instrucciones especiales...'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class AnalisisAsignadoForm(forms.ModelForm):
    """
    Formulario para asignar análisis
    """
    class Meta:
        model = AnalisisAsignado
        fields = ['analisis', 'instrucciones', 'observaciones', 'fecha_programada']
        widgets = {
            'analisis': forms.Select(attrs={
                'class': 'form-select'
            }),
            'instrucciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Instrucciones para el análisis...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales...'
            }),
            'fecha_programada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        } 