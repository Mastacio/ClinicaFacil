
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import PacienteRegistroForm, CustomLoginForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

@login_required(login_url='/login/')
def welcome(request):
    return render(request, 'users/welcome.html')

def registro(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    if request.method == 'POST':
        form = PacienteRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = PacienteRegistroForm()
    return render(request, 'users/registro.html', {'form': form})

def error_403(request, exception=None):
    """
    Vista para manejar errores de permisos (403)
    """
    return render(request, 'users/error_403.html', status=403)
