from django.http import HttpResponse
from django.shortcuts import render
from warung.models import Warung
from menu.models import Menu
from django.core import serializers
from django.db.models import Avg
from ratereview.models import Review

# Create your views here.
def show_main(request):
    warung_registered = Warung.objects.all()
    context={
        "warung_entries":warung_registered
    }

    return render(request, "allwarung.html", context)

def show_warung(request, namawarung):
    warung_shown = Warung.objects.filter(nama=namawarung)
    menus = Menu.objects.filter(warung=namawarung)
    
    # Calculate the average rating for each menu item
    menu_with_reviews = []
    for menu in menus:
        avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
        menu_with_reviews.append({
            'menu': menu,
            'avg_rating': avg_rating
        })
    
    # Calculate the overall average rating for the warung
    warung_avg_rating = Review.objects.filter(menu__warung=namawarung).aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        "warung_entries": warung_shown,
        "menu_entries": menu_with_reviews,
        "warung_avg_rating": warung_avg_rating,
    }
    return render(request, "warung.html", context)