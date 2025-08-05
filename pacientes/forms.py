from django import forms

from django.contrib.auth import get_user_model
from .models import PacientePerfil

User = get_user_model()

class CrearPacienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, initial='12345678', label='Contraseña inicial')
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
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_sangre': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'enfermedades_cronicas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'medicamentos': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'antecedentes_quirurgicos': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'antecedentes_familiares': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
