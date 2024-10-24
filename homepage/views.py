from django.shortcuts import render
from menu.models import Menu

# Create your views here.
def show_main(request):
    # Mengambil 3 menu acak dari model Menu di aplikasi menu
    random_menu = Menu.objects.order_by('?')[:3]
    
    context = {
        'menus': random_menu,
    }
    return render(request, 'homepage.html', context)
