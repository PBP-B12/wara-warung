from django.http import HttpResponse
from django.shortcuts import render
from warung.models import Warung
from menu.models import Menu
from django.core import serializers

# Create your views here.
def show_main(request):
    warung_registered = Warung.objects.all()
    context={
        "warung_entries":warung_registered
    }

    return render(request, "allwarung.html", context)

def show_warung(request, namawarung):
    warung_shown = Warung.objects.filter(nama=namawarung)
    menus=Menu.objects.filter(warung=namawarung)
    context={
        "warung_entries":warung_shown,
        "menu_entries":menus
    }
    return render(request, "warung.html", context)