from django.shortcuts import render
from .models import CompanyService  # Ensure correct import path

def services(request):
    services_datas = CompanyService.objects.all()  # Fetch all services
    return render(request, 'services.html', {'services_datas': services_datas})
