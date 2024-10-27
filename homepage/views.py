from django.shortcuts import render
from menu.models import Menu
import random
from django.http import JsonResponse
from warung.models import Warung
from ratereview.models import Review
from django.db.models import Avg

# Create your views here.
def show_main(request):
    all_menu = list(Menu.objects.all())
    random_menu = random.sample(all_menu, 3)  # Mengambil 3 menu acak
    menu_with_reviews = []
    for menu in random_menu:
        avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
        menu_with_reviews.append({
            'menu': menu,
            'avg_rating': avg_rating
        })

    context = {
        'menus': menu_with_reviews,
    }

    return render(request, "homepage.html", context)

def get_warungs(request):
    warungs = Warung.objects.all().values('id', 'nama')
    return JsonResponse({'warungs': list(warungs)})