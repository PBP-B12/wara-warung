from django.http import JsonResponse
from django.shortcuts import render
from menu.models import Menu
from ratereview.models import Review
from django.db.models import Avg

def search_menu(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')  # Get search query
        budget = request.GET.get('budget', '')  # Get selected budget
        
        # Filter menus by name
        results = Menu.objects.all()
        if query:
            results = results.filter(menu__icontains=query)

        # Filter by budget if provided
        if budget:
            results = results.filter(harga__lte=int(budget))
        
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
        
        return JsonResponse({'results': data})
    return render(request, 'search.html')
