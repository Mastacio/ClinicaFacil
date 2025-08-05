from django.shortcuts import render
from .models import ClinicInfo

def home(request):
    clinic = ClinicInfo.objects.first()
    return render(request, 'core/home.html', {'clinic': clinic})
