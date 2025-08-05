
from django.urls import path

from django.contrib.auth.views import LogoutView
from .views import welcome, registro, error_403, CustomLoginView


class CustomLogoutView(LogoutView):
    next_page = '/login/'
    def get(self, request, *args, **kwargs):
        """Permitir logout por GET para facilitar el cierre de sesión desde un enlace."""
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', registro, name='registro'),
    path('panel/', welcome, name='welcome'),
    path('error/403/', error_403, name='error_403'),
]
