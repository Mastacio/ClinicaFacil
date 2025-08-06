from django import forms
from users.models import User
from .models import DoctorPerfil, Especialidad, HorarioDoctor

class HorarioDoctorForm(forms.ModelForm):
    class Meta:
        model = HorarioDoctor
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'intervalo_minutos']
        widgets = {
            'dia_semana': forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'intervalo_minutos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 180, 'step': 1}),
        }

class CrearDoctorForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nombre(s)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))
    identificacion = forms.CharField(label='Identificación', widget=forms.TextInput(attrs={'class': 'form-control'}))
    especialidades = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Especialidades'
    )

    class Meta:
        model = DoctorPerfil
        fields = ['identificacion', 'telefono', 'direccion', 'registro_medico', 'universidad', 'anios_experiencia', 'especialidades']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'universidad': forms.TextInput(attrs={'class': 'form-control'}),
            'anios_experiencia': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo.')
        return email

    def save(self, commit=True):
        # Crear usuario y perfil
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password='1234567890',
            role='doctor',
            is_active=True
        )
        perfil = super().save(commit=False)
        perfil.user = user
        if commit:
            perfil.save()
            self.save_m2m()
        return perfil
