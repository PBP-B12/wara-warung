import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from menu.models import Menu
from menu.forms import MenuForm
from django.core import serializers
from warung.models import Warung  # Import the Warung model from warung app
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Avg
from ratereview.models import Review

def show_main(request):
    # Fetch all menu entries with their average ratings
    menu_with_reviews = []
    for menu in Menu.objects.all():
        avg_rating = Review.objects.filter(menu=menu).aggregate(Avg('rating'))['rating__avg'] or 0
        menu_with_reviews.append({
            'menu': menu,
            'avg_rating': avg_rating
        })

    context = {
        'menu_entries': menu_with_reviews,
    }

    return render(request, "allmenu.html", context)

def edit_menu(request, id):
    # Get the menu entry based on the id
    menu = Menu.objects.get(pk = id)
    
    # Set the menu entry as an instance of the form
    form = MenuForm(request.POST or None, instance=menu)
    
    # Get all warungs to be displayed in the dropdown
    warungs = Warung.objects.all()

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('homepage:show_main'))

    context = {
        'form': form,
        'warungs': warungs,  # Pass warungs to the template
    }
    if request.GET.get('json') != None:
        return JsonResponse({"status" : 200})
    return render(request, "edit_menu.html", context)

def delete_menu(request, id):
    menus = Menu.objects.get(pk = id)
    menus.delete()
    return HttpResponseRedirect(reverse('homepage:show_main'))

def delete_menu_json(request,id):
    menus = Menu.objects.get(pk = id)
    menus.delete()
    return JsonResponse({"status" : 200})

def show_xml(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_flutter(request):
    results = Menu.objects.all()
    username = request.user.username
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

def add_menu(request):
    form = MenuForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('menu:show_main')

    context = {'form': form}
    return render(request, "add_menu.html", context)

@csrf_exempt
@require_POST
def add_menu_ajax(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Menu added successfully!"}, status=200)
        return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def get_warungs(request):
    if request.method == "GET":
        warungs = Warung.objects.all()
        data = [
            {
                "id": warung.id,
                "nama": warung.nama,
            }
            for warung in warungs
        ]
        return JsonResponse({"dropdown_warungs": data}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def add_menu_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_menu = Menu.objects.create(
            warung=data["warung"],
            menu=data["menu"],
            harga=int(data["harga"]),
            gambar=data["gambar"],
        )

        new_menu.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_menu_flutter(request, id):
    if request.method == 'POST':

        data = json.loads(request.body)

        # Get the existing menu item
        menu = Menu.objects.get(pk=id)

        # Update the fields directly on the instance
        menu.warung = data["warung"]
        menu.menu = data["menu"]
        menu.harga = int(data["harga"])
        menu.gambar = data["gambar"]

        # Save the updated instance
        menu.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
