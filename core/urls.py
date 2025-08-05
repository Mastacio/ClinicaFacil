"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import home
from users.views import error_403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('users.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('doctores/', include('doctores.urls')),
    path('citas/', include('citas.urls')),
    path('gestion/', include('gestion.urls')),
]

# Handlers de error
handler403 = 'users.views.error_403'
