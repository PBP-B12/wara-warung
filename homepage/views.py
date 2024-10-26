from django.shortcuts import render
from menu.models import Menu
import random
from django.http import JsonResponse
from warung.models import Warung

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "homepage.html", context)

def get_warungs(request):
    warungs = Warung.objects.all().values('id', 'nama')
    return JsonResponse({'warungs': list(warungs)})
