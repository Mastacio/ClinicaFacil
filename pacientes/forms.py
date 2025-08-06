from django import forms

from django.contrib.auth import get_user_model
from .models import PacientePerfil

User = get_user_model()

class CrearPacienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), initial='12345678', label='Contraseña inicial')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Correo electrónico')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.role = 'paciente'
        if commit:
            user.save()
        return user

class PacientePerfilForm(forms.ModelForm):
    class Meta:
        model = PacientePerfil
        exclude = ['user', 'completado']
        widgets = {
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9, DNI 12345678, etc.'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Selecciona la fecha de nacimiento'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el sexo'
            }),
            'tipo_sangre': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el tipo de sangre'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +1234567890'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad de residencia'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País'
            }),
            'contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto de emergencia'
            }),
            'telefono_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de emergencia'
            }),
            'alergias': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describe las alergias conocidas...'
            }),
            'enfermedades_cronicas': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describe las enfermedades crónicas...'
            }),
            'medicamentos': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Lista los medicamentos actuales...'
            }),
            'antecedentes_quirurgicos': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describe los antecedentes quirúrgicos...'
            }),
            'antecedentes_familiares': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describe los antecedentes familiares relevantes...'
            }),
            'notas': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control',
                'placeholder': 'Notas adicionales...'
            }),
        }
