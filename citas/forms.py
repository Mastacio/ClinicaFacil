from django import forms
from .models import Cita
from pacientes.models import PacientePerfil
from doctores.models import DoctorPerfil, Consultorio

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'doctor', 'consultorio', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'notas']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select', 'data-live-search': 'true'}),
            'doctor': forms.Select(attrs={'class': 'form-select', 'data-live-search': 'true'}),
            'consultorio': forms.Select(attrs={'class': 'form-select', 'data-live-search': 'true'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        
        # Cargar pacientes y doctores disponibles
        self.fields['paciente'].queryset = PacientePerfil.objects.select_related('user').all()
        self.fields['doctor'].queryset = DoctorPerfil.objects.filter(activo=True).select_related('user')
        self.fields['consultorio'].queryset = Consultorio.objects.filter(activo=True)
        
        # Personalizar las etiquetas
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.user.email})"
        self.fields['doctor'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.user.email})"
        self.fields['consultorio'].label_from_instance = lambda obj: f"{obj.nombre} - {obj.ubicacion}" if obj.ubicacion else obj.nombre
        
        if initial.get('paciente'):
            self.fields['paciente'].required = True
        if initial.get('doctor'):
            self.fields['doctor'].required = True
