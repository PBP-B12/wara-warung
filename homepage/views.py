from django.shortcuts import render
from menu.models import Menu
import random
from django.http import JsonResponse
from warung.models import Warung

# Create your views here.
def show_main(request):
    all_menu = list(Menu.objects.all())
    random_menu = random.sample(all_menu, 3)  # Mengambil 3 menu acak
    context = {
        'menus': random_menu,
    }

    return render(request, "homepage.html", context)

def get_warungs(request):
    warungs = Warung.objects.all().values('id', 'nama')
    return JsonResponse({'warungs': list(warungs)})