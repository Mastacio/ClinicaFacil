from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'doctor', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'notas']
        widgets = {
                'paciente': forms.Select(attrs={'class': 'form-select select2-ajax-paciente', 'data-live-search': 'true'}),
                'doctor': forms.Select(attrs={'class': 'form-select select2-ajax-doctor', 'data-live-search': 'true'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        if initial.get('paciente'):
            self.fields['paciente'].required = True
        if initial.get('doctor'):
            self.fields['doctor'].required = True
