from django.http import JsonResponse
from django.shortcuts import render
from menu.models import Menu
from ratereview.models import Review
from django.db.models import Avg
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt

def search_menu(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('json') != None:
        username = request.user.username  # Accessing the 'username' directly from the User object

        query = request.GET.get('query', '')  # Get search query
        budget = request.GET.get('budget', '')  # Get selected budget
        warung = request.GET.get('warung', '')
        results = Menu.objects.all()
        if query:
            results = results.filter(menu__icontains=query)

        if budget:
            results = results.filter(harga__lte=int(budget))
        
        if warung:
            results = results.filter(warung__icontains=warung)
        
        data = []
        for menu in results:
            avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
            data.append({
                'menu': menu.menu,
                'harga': menu.harga,
                'warung': menu.warung,
                'gambar': menu.gambar,
                'id': menu.id,
                'avg_rating': round(avg_rating, 1)  # One decimal place
            })
        response = JsonResponse({'results': data, 'username': username})
        return response
    return render(request, 'search.html')

@csrf_exempt
def menu_data_flutter(request):
    if request.method == 'POST':
        data_req = json.loads(request.body)
        username = request.user.username
        query = data_req['query']
        budget = data_req['budget']
        warung = data_req['warung']
        results = Menu.objects.all()
        if query:
            results = results.filter(menu__icontains=query)

        if budget:
            results = results.filter(harga__lte=int(budget))
        
        if warung:
            results = results.filter(warung__icontains=warung)
        
        data = []
        for menu in results:
            avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
            data.append({
                'menu': menu.menu,
                'harga': menu.harga,
                'warung': menu.warung,
                'gambar': menu.gambar,
                'id': menu.id,
                'avg_rating': round(avg_rating, 1)  # One decimal place
            })
        response = JsonResponse({'results': data, 'username': username})
        return response