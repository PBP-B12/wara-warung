# views.py
from django.http import JsonResponse
from django.shortcuts import render
from menu.models import Menu

def search_menu(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        results = Menu.objects.filter(menu__icontains=query)
        data = [{'menu': menu.menu, 'harga': menu.harga, 'warung': menu.warung, 'gambar': menu.gambar} for menu in results]
        return JsonResponse({'results': data})
    return render(request, 'search.html')
