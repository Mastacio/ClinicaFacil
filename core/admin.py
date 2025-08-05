from django.contrib import admin
from .models import ClinicInfo

@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
