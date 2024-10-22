from django.shortcuts import render
from menu.models import Menu

# Create your views here.
def show_main(request):
    menu_entries = Menu.objects.all()
    context={
        "menu_entries":menu_entries
    }

    return render(request, "main.html", context)